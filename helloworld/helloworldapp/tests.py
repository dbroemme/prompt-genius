from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from .models import Quiz, Question, Answer
from .services import create_question_with_answers
from .services import create_question_with_answers_from_xml


class QuestionCreationTestCase(TestCase):
    def setUp(self):
        self.quiz = Quiz.objects.create(name='Quiz', topic='Topic')
        self.text = '''
<response>
  <question>Which planet is the hottest in our solar system?</question>
  <a>Mercury</a>
  <b>Venus</b>
  <c>Earth</c>
  <d>Mars</d>
  <correct_answer>B</correct_answer>
</response>
        '''

    def test_create_question_with_answers(self):
        question = create_question_with_answers_from_xml(self.text, self.quiz)

        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Answer.objects.count(), 4)

        self.assertEqual(question.quiz, self.quiz)
        self.assertEqual(question.text, "Which planet is the hottest in our solar system?")

        correct_answer = Answer.objects.get(question=question, is_correct=True)
        self.assertEqual(correct_answer.text, "Venus")

        answer_texts = ["Mercury", "Venus", "Earth", "Mars"]
        for answer_text in answer_texts:
            answer = Answer.objects.get(question=question, text=answer_text)
            if answer_text == "Venus":
                self.assertTrue(answer.is_correct)
            else:
                self.assertFalse(answer.is_correct)


class QuizListViewTestCase(TestCase):
    def setUp(self):
        self.quiz1 = Quiz.objects.create(name='Quiz 1', topic='Topic 1')
        self.quiz2 = Quiz.objects.create(name='Quiz 2', topic='Topic 2')

    def test_quiz_list_view(self):
        response = self.client.get(reverse('quiz_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_list.html')
        self.assertContains(response, self.quiz1.name)
        self.assertContains(response, self.quiz1.topic)
        self.assertContains(response, self.quiz2.name)
        self.assertContains(response, self.quiz2.topic)

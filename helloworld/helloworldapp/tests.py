from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import Quiz, Question, Answer
from .services import create_question_with_answers

class QuestionCreationTestCase(TestCase):

    def setUp(self):
        self.quiz = Quiz.objects.create(name='Science Quiz', topic='Science')

    def test_create_question_with_answers(self):
        # Define the sample text data
        text_data = "Question: What is the primary source of energy for the Earth?\n" \
                    "A) Solar energy\n" \
                    "B) Wind energy\n" \
                    "C) Nuclear energy\n" \
                    "D) Geothermal energy\n" \
                    "Correct answer: A (Solar Energy)"

        # Call the create_question_with_answers function
        question = create_question_with_answers(text_data, self.quiz)

        # Assertions to verify the behavior
        self.assertIsInstance(question, Question)
        self.assertEqual(question.text, "What is the primary source of energy for the Earth?")

        answers = Answer.objects.filter(question=question)
        self.assertEqual(len(answers), 4)

        correct_answer = Answer.objects.get(question=question, is_correct=True)
        self.assertEqual(correct_answer.text, "A) Solar energy")

        incorrect_answers = Answer.objects.filter(question=question, is_correct=False)
        self.assertEqual(len(incorrect_answers), 3)

        # Add additional assertions as needed


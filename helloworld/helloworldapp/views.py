from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from .forms import QuizForm
from .models import Quiz, Question, Answer
from .services import generate_question, create_question_with_answers_from_xml


from django.shortcuts import render, redirect
from .forms import QuizForm
from .services import generate_question, create_question_with_answers_from_xml

def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save()

            # Generate and parse multiple questions
            num_questions = 5
            topic = quiz.topic

            for _ in range(num_questions):
                xml_data = generate_question(topic)
                create_question_with_answers_from_xml(xml_data, quiz)

            return redirect('quiz_created')  # Redirect to success page
    else:
        form = QuizForm()

    return render(request, 'create_quiz.html', {'form': form})


def quiz_created(request):
    return render(request, 'quiz_created.html')

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})


def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.questions.all()
    total_questions = questions.count()
    correct_answers = 0

    if request.method == 'POST':
        # Handle form submission
        for question in questions:
            user_answer = request.POST.get(str(question.id))
            if user_answer:
                answer = get_object_or_404(Answer, pk=user_answer)
                if answer.is_correct:
                    correct_answers += 1

        # Calculate quiz score or perform any desired logic
        score = (correct_answers / total_questions) * 100

        # Render result template with the quiz score
        return render(request, 'quiz_result.html', {'quiz': quiz, 'score': score})

    # Render the quiz form template with the questions and possible answers
    return render(request, 'take_quiz.html', {'quiz': quiz, 'questions': questions})

from django.shortcuts import render

def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.questions.all()
    total_questions = questions.count()
    correct_answers = 0

    # Perform any necessary calculations to determine the number of correct answers
    # You should have this logic implemented based on your specific requirements

    # Calculate the score as a percentage
    score = (correct_answers / total_questions) * 100

    return render(request, 'quiz_result.html', {'quiz': quiz, 'questions': questions, 'correct_answers': correct_answers, 'score': score})

def main_menu(request):
    return render(request, 'menu.html')

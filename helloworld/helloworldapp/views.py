from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.shortcuts import render, redirect
from .forms import QuizForm
from .services import generate_question, create_question_with_answers


def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save()  # Save the quiz instance
            topic = quiz.topic  # Get the topic from the quiz

            # Generate a question for the quiz
            question_text = generate_question(topic)
            print("The question from Bard is")
            print(question_text)

            # Create the question and associated answers
            question = create_question_with_answers(question_text, quiz)
            question.save()

            return redirect('quiz_created')
    else:
        form = QuizForm()

    return render(request, 'create_quiz.html', {'form': form})


def quiz_created(request):
    return render(request, 'quiz_created.html')

def main_menu(request):
    return render(request, 'menu.html')

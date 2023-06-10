from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.shortcuts import render, redirect
from .forms import QuizForm
from .models import Quiz
from .services import generate_question, create_question_with_answers_from_xml


from django.shortcuts import render, redirect
from .forms import QuizForm
from .services import generate_question, create_question_with_answers_from_xml

def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save()

            # Generate question and parse data
            topic = quiz.topic
            xml_data = generate_question(topic)
            question = create_question_with_answers_from_xml(xml_data, quiz)

            return redirect('quiz_created')  # Redirect to success page
    else:
        form = QuizForm()

    return render(request, 'create_quiz.html', {'form': form})


def quiz_created(request):
    return render(request, 'quiz_created.html')

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

def main_menu(request):
    return render(request, 'menu.html')

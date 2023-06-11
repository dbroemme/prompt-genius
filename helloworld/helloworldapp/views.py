# Create your views here.
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from .forms import QuizForm
from .models import Quiz, Question, Answer
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
    if not request.user.is_authenticated:
        return register(request)

    if 'current_question_index' in request.session:
        print("Removing current question index from session")
        del request.session['current_question_index']
    if 'correct_answers' in request.session:
        print("Removing correct answers from session")
        del request.session['correct_answers']
    display_session_keys(request)
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.questions.all()
    total_questions = questions.count()
    current_question_index = request.session.get('current_question_index', 0)
    correct_answers = request.session.get('correct_answers', 0)

    if request.method == 'POST':
        user_answer = request.POST.get('answer')

        if user_answer:
            current_question = questions[current_question_index]
            answer = get_object_or_404(Answer, pk=user_answer)

            if answer.is_correct:
                correct_answers += 1

        current_question_index += 1
        request.session['current_question_index'] = current_question_index
        request.session['correct_answers'] = correct_answers

        if current_question_index >= total_questions:
            return redirect('quiz_result', quiz_id=quiz_id)

    else:
        if 'current_question_index' in request.session:
            del request.session['current_question_index']
        if 'correct_answers' in request.session:
            del request.session['correct_answers']

    current_question = questions[current_question_index]

    context = {
        'quiz': quiz,
        'question': current_question,
        'current_question_index': current_question_index + 1,
        'total_questions': total_questions,
    }

    return render(request, 'take_quiz.html', context)

def display_session_keys(request):
    for a_key in request.session.keys():
        print("Session " + a_key + ": " + str(request.session[a_key]))

def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    total_questions = quiz.questions.count()
    correct_answers = int(request.session['correct_answers'])

    # Perform any necessary calculations to determine the number of correct answers
    # You should have this logic implemented based on your specific requirements

    # Calculate the score as a percentage
    score = (correct_answers / total_questions) * 100

    context = {
        'quiz': quiz,
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'score': score,
    }

    return render(request, 'quiz_result.html', context)

def main_menu(request):
    return render(request, 'menu.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to the desired page after successful login
            return redirect('quiz_list')
        else:
            # Authentication failed
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'login.html')

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the desired page after successful registration
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    # Redirect to the desired page after logout
    return redirect('login')


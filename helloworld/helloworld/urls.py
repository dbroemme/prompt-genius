"""
URL configuration for helloworld project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from helloworldapp.views import main_menu, create_quiz, quiz_created
from helloworldapp.views import quiz_list, take_quiz, quiz_result

urlpatterns = [
    path('', quiz_list, name='quiz_list'),
    path('quiz-list/', quiz_list, name='quiz_list'),
    path('create-quiz/', create_quiz, name='create_quiz'),
    path('quiz-created/', quiz_created, name='quiz_created'),
    path('admin/', admin.site.urls),
    path('quizzes/<int:quiz_id>/', take_quiz, name='take_quiz'),
    path('quiz-result/', quiz_result, name='quiz_result'),
]

from django.db import models

# Create your models here.
class Quiz(models.Model):
    name = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    option = models.TextField(null=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Participant(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name if self.name else str(self.id)

class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results')
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='results')
    score = models.IntegerField()

    def __str__(self):
        return f"{self.quiz.name} - {self.participant}"

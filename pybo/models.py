from django.db import models


# Create your models here.

#질문 모델
class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject


#답변 모델
class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers'
    )
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        title = self.question.subject+"의 답변(id="+str(self.id)+")"
        return title




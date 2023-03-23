from django.contrib.auth.models import User
from django.db import models

# Model politika
class Politician(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=25)
    position = models.CharField(max_length=35)

    intercessors = models.ManyToManyField(User, blank=True)# Přímluvci

    def __str__(self):
        return self.name + " " + self.surname

#Volby zpětné vazby
feedback_subject_choices = (
    ("v", "Návrh na vylepšení"),
    ("p", "Problém"),
    ("j", "Něco jiného")
)

# Modely ukládané do databáze
class Feedback(models.Model):  # Zpětná vazba
    e_mail = models.EmailField()
    subject = models.CharField(max_length=1, choices=feedback_subject_choices, default="v")
    text = models.TextField()
    date_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.text
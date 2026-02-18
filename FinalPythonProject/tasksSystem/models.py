from django.db import models
import datetime
class Team(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id}. {self.name}"
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    fullName = models.CharField(max_length=20)
    password = models.CharField(max_length=10)
    phone = models.CharField(max_length=10)
    isAdmin = models.BooleanField(default=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50,default='')
    status = models.CharField(max_length=10, default='new')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    finalDate = models.DateField(default=datetime.date.today(), null=True,blank=True)

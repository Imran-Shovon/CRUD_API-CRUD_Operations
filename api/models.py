from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=50)
    roll = models.IntegerField()
    city = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} "

    # # def get_absolute_url(self):
    # #     return reverse("api:home", kwargs={"id": self.id})


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Department(models.Model):
    dept_name = models.CharField(max_length=50)
    dept_code = models.IntegerField()

    def __str__(self):
        return f"{self.dept_name} "


class StuDept(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student} ({self.dept}) "

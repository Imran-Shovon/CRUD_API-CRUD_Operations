from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Department, Student, StuDept


class AddStudent(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('name', 'roll', 'city')


class AddDepartment(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('dept_name', 'dept_code')


class AddStuDept(forms.ModelForm):
    class Meta:
        model = StuDept
        fields = ('student', 'dept')


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

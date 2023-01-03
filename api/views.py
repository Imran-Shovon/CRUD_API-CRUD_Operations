from audioop import reverse

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout  # add this
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.contrib.auth.models import User, auth
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView, ListView
from rest_framework import authentication, permissions
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
# Create your views here.
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import AddDepartment, AddStudent, AddStuDept, NewUserForm
from .models import Department, Student, StuDept
from .serializers import StudentSerializer


def signup(request):
    # return render(request, template_name = 'api/registration.html')
    return redirect('register')


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('login')
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="api/registration.html", context={"register_form": form})


# def register_request(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         email = request.POST['email']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']
#         if password1 == password2:
#             if User.objects.filter(username=username).exists():
#                 messages.info(request, "Username already in use")
#                 return redirect('signup')

#             elif User.objects.filter(email=email).exists():
#                 messages.info(request, "Email already in use")
#                 return redirect('signup')
#             else:
#                 user = User.objects.create_user(
#                     username=username, email=email, password='password1')
#                 user.save()
#                 messages.success(request, "Registration successful.")
#                 return redirect("login")
#         else:
#             messages.success(request, "Password not matching")
#             print("Registration failed")

#     form = NewUserForm()
#     return render(request=request, template_name="api/registration.html", context={"register_form": form})


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def permissions(request, format=None):
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
    }
    return Response(content)


# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, "Login successful.")
#             return redirect('home-page')

#         else:
#             messages.success(request, "Username or password error occured.")
#             return redirect('login')
#     else:
#         return render(request, 'api/login.html', {})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home-page")
            else:
                messages.error(request, "User not approved.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="api/login.html", context={"login_form": form})


def logout_view(request):
    logout(request)
    messages.info('You have been logged out')
    return redirect('login')


class ListStudentView(GenericAPIView, ListModelMixin):
    #template_name = 'api/home.html'
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


def add_show(request):
    if request.method == "POST":
        fm = AddStudent(request.POST)
        if fm.is_valid():
            nm = fm.cleaned_data['name']
            em = fm.cleaned_data['email']
            pw = fm.cleaned_data['password']
            reg = Student(name=nm, email=em, password=pw)
            reg.save()
            fm = AddStudent()
    else:
        fm = AddStudent()
    stud = Student.objects.all()
    return render(request, 'api/home.html', {
        'form': fm,
        'stu': stud,
    })


class CreateStudentView(GenericAPIView, CreateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


def addstudent(request):
    if request.method == "POST":
        fm = AddStudent(request.POST)
        if fm.is_valid():
            nm = fm.cleaned_data['name']
            roll = fm.cleaned_data['roll']
            city = fm.cleaned_data['city']
            reg = Student(name=nm, roll=roll, city=city)
            reg.save()
            messages.success(request, "Student has been successfully saved")
            fm = AddStudent()
    else:
        fm = AddStudent()
    stud = Student.objects.all()
    return render(request, 'api/addstudent.html', {
        'form': fm,
        'stu': stud,
    })


class UpdateStudentView(GenericAPIView, UpdateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


def update_student(request, id):
    if request.method == "POST":
        pi = Student.objects.get(pk=id)
        fm = AddStudent(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
            messages.success(request, "Student has been successfully Updated")
    else:
        pi = Student.objects.get(pk=id)
        fm = AddStudent(instance=pi)
    return render(request, 'api/update.html', {
        'form': fm,
        'id': id,
    })


class DeleteStudentView(GenericAPIView, DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def delete(self, request, *args, **kwargs):
        res = {"msg": "Data deleted"}
        # response = JSONRenderer().render(res)
        # print("response: ", response)
        # response = json_data
        self.destroy(request, *args, **kwargs)
        return JsonResponse(res)


def delete_student(request, id):
    if request.method == "POST":
        pi = Student.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect("/home/")


# Department views Starts here...

# See all the departments here.
def department_view(request):
    if request.method == "POST":
        fm = AddDepartment(request.POST)
        if fm.is_valid():
            dn = fm.cleaned_data['dept_name']
            dc = fm.cleaned_data['dept_code']
            reg = Department(dept_name=dn, dept_code=dc)
            reg.save()
            fm = AddDepartment()

    else:
        fm = AddDepartment()
    dept = Department.objects.all()
    return render(request, 'api/departments.html', {
        'form': fm,
        'dept': dept
    })

# Adding New Department


def adddepartment(request):
    if request.method == 'POST':
        fm = AddDepartment(request.POST)
        print("inside")
        if fm.is_valid():
            print("inside valid")
            dn = fm.cleaned_data['dept_name']
            dc = fm.cleaned_data['dept_code']
            print(dn, dc)
            reg = Department(dept_name=dn, dept_code=dc)
            reg.save()
            messages.success(request, 'Department has been Added')
            fm = AddDepartment()
    else:
        fm = AddDepartment()
    dept = Department.objects.all()
    return render(request, 'api/adddepartment.html', {
        'form': fm,
        'dept': dept
    })


# Update the Existing Department

def update_department(request, id):
    if request.method == "POST":
        pi = Department.objects.get(pk=id)
        fm = AddDepartment(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
            messages.success(
                request, "Depaertment has been successfully Updated")
    else:
        pi = Department.objects.get(pk=id)
        fm = AddDepartment(instance=pi)
    return render(request, 'api/updatedept.html', {
        'form': fm,
        'id': id,
    })


# Delete department


def delete_department(request, id):
    if request.method == "POST":
        pi = Department.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect("/department/")


# Adding Studnet and department Starts here....

# See all the departments here.
def department_student_view(request):
    if request.method == "POST":
        fm = AddStuDept(request.POST)
        if fm.is_valid():
            dn = fm.cleaned_data['student']
            dc = fm.cleaned_data['dept']
            reg = StuDept(dept_name=dn, dept_code=dc)
            reg.save()
            fm = AddStuDept()

    else:
        fm = AddStuDept()
    dept = StuDept.objects.all()
    return render(request, 'api/student_department.html', {
        'form': fm,
        'dept': dept
    })

# Adding Existing students departments


def addstudentdepartment(request):
    if request.method == 'POST':
        # fm = AddDepartment(request.POST)
        student = request.POST.get('student')
        department = request.POST.get('dept')
        print("Adding student department", student, department)
        fm = AddStuDept(request.POST)
        print("I am here")
        if StuDept.objects.filter(student=student).exists():
            print("Before")
            fm.save()
            print("After")
            messages.success(
                request, "Student's Department has been Added")
            fm = AddStuDept()

        else:
            messages.error(request, "Student does not exist")
            fm = AddStuDept()

    else:
        fm = AddStuDept()
    dept = StuDept.objects.all()
    return render(request, 'api/add_student_department.html', {
        'update_form': fm,
        'dept': dept
    })


# def addstudentdepartment(request):
#     if request.method == 'POST':
#         print("Adding student department")
#         fm = AddStuDept(request.POST)
#         if fm.is_valid():
#             print("Inside Validation")
#             stu = fm.cleaned_data['student']
#             dpt = fm.cleaned_data['dept']
#             print(stu, dpt)
#             stu_data = StuDept.objects.filter(student=stu)
#             if stu_data is not None:
#                 reg = StuDept(student=stu, dept=dpt)
#                 reg.save()
#                 messages.success(
#                     request, "Student's Department has been Added")
#                 fm = AddStuDept()
#             else:
#                 messages.error(
#                     request, "Student's Department data doesn't exists")
#                 fm = AddStuDept()
#     else:
#         fm = AddStuDept()
#     dept = StuDept.objects.all()
#     return render(request, 'api/add_student_department.html', {
#         'form': fm,
#         'dept': dept
#     })


# def addstudentdepartment(request):
#     if request.method == 'POST':
#         print("Adding student department")
#         fm = AddStuDept(request.POST)
#         if fm.is_valid():
#             print("Inside Validation")
#             stu = fm.cleaned_data['student']
#             dpt = fm.cleaned_data['dept']
#             print(stu, dpt)
#             stu_data = StuDept.objects.filter(student=stu)
#             if stu_data is not None:
#                 reg = StuDept(student=stu, dept=dpt)
#                 reg.save()
#                 messages.success(
#                     request, "Student's Department has been Added")
#                 fm = AddStuDept()
#             else:
#                 messages.error(
#                     request, "Student's Department data doesn't exists")
#                 fm = AddStuDept()
#     else:
#         fm = AddStuDept()
#     dept = StuDept.objects.all()
#     return render(request, 'api/add_student_department.html', {
#         'update_form': fm,
#         'dept': dept
#     })


def update_student_department(request, id):
    if request.method == "POST":
        pi = StuDept.objects.get(pk=id)
        fm = AddStuDept(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
            messages.success(
                request, "Depaertment has been successfully Updated")
    else:
        
        pi = StuDept.objects.get(pk=id)
        fm = AddStuDept(instance=pi)
    return render(request, 'api/update_student_department.html', {
        'form': fm,
        'id': id,
    })

# Delete department


def delete_student_department(request, id):
    if request.method == "POST":
        pi = StuDept.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect("/department-student")

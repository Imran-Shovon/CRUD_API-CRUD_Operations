from django.urls import path

from . import views

urlpatterns = [
    # Api view
    path('studentlist/', views.ListStudentView.as_view(), name='students'),
    path('addstudentapi', views.CreateStudentView.as_view(), name='addstudent'),

    path('updatestudentapi/<int:pk>',
         views.UpdateStudentView.as_view(), name='UpdateStudent'),
    path('deletestudent/<int:pk>',
         views.DeleteStudentView.as_view(), name='DeleteStudent'),

    # Html page rendering.
    path('home/', views.add_show, name='home-page'),
    path('addstudent/', views.addstudent, name="add-student"),
    path('updatestudent/<int:id>', views.update_student, name='update'),
    path('delete/<int:id>', views.delete_student, name='delete'),
    #     path('loginpage/', views.loginpage, name='login-page'),
    path('', views.user_login, name='login'),
    path('', views.logout_view, name='logout'),
    path('register/', views.register_request, name='register'),
    path('signup/', views.signup, name='signup'),
    path('permissions/', views.permissions, name='permissions'),

    # Department urls
    path('department/', views.department_view, name='department'),
    path('adddepartment/', views.adddepartment, name='add-department'),
    path('updatedepartment/<int:id>',
         views.update_department, name='update-department'),
    path('deletedept/<int:id>', views.delete_department, name='delete-dept'),

    # Adding student and department urls Starts here.
    path('department-student', views.department_student_view,
         name='department-student'),
    path('addstudentdepartment', views.addstudentdepartment,
         name='add-student-department'),
    path('update_student_department/<int:id>', views.update_student_department,
         name='update-student-department'),
    path('delete_student_department/<int:id>',
         views.delete_student_department, name='delete_student_department'),

]

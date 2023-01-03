from django.contrib import admin

from .models import Department, Student, StuDept

# Register your models here.


class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', "name", 'roll', 'city']


admin.site.register(Student, StudentAdmin)
admin.site.register(Department)
admin.site.register(StuDept)

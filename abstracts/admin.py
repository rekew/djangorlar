#django modules
from django.contrib import admin
from .models import Student, Course

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "is_deleted", "deleted_at")
    list_filter = ("is_deleted",)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "is_deleted", "deleted_at")
    list_filter = ("is_deleted",)

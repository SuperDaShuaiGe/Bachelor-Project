from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')


class CoursesAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'name', 'guide', 'file')


class SelectionAdmin(admin.ModelAdmin):
    list_display = ('course', 'students')


admin.site.register(User, UserAdmin)
admin.site.register(Courses, CoursesAdmin)
admin.site.register(Selection, SelectionAdmin)
admin.site.site_title = 'Management'

admin.site.site_header = 'Management'
admin.site.unregister(Group)
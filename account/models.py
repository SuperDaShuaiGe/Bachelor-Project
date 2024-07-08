from django.db import models

from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        # Return a more descriptive name
        return f"{self.username} ({'Teacher' if self.is_teacher else 'Student'})"


class Courses(models.Model):
    teacher = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='teacher')
    name = models.CharField(max_length=255, verbose_name='name')
    guide = models.TextField(verbose_name='description', default='no guide!')
    file = models.FileField(upload_to='media/', null=True, blank=True)

    class Meta:
        db_table = 'courses'

    def __str__(self):
        # Returns the course name and the name of the teacher
        return f"{self.name} - Taught by {self.teacher.username}"

class Selection(models.Model):
    course = models.ForeignKey(to=Courses, on_delete=models.CASCADE)
    students = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='student')
    file = models.FileField(upload_to='media/', null=True, blank=True)
    backward = models.TextField(verbose_name='backward', default='no backward!')

    class Meta:
        db_table = 'Selection'

    def __str__(self):
        # Returns course selection information, including student name and course title
        return f"{self.students.username} selected {self.course.name}"
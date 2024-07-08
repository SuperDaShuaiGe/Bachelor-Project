import os.path
import time

from django.http import HttpResponse
from ChatDjango import settings
from ChatDjango.settings import BASE_DIR
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import UserLoginForm
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .models import Courses, Selection  # Ensure you have a Course model
from .utils import read_docx, get_response, read_pdf, read_cpp_with_newlines

def index(request):
    if request.user.is_authenticated:

        if request.user.is_teacher:
            return redirect('teacher_dashboard')
        return redirect('student_dashboard')

    return redirect('/accounts/login')  # Redirect users to the login page when they access the index page

def user_login(request):
    if request.method == 'POST':  # Check if the form was submitted
        form = UserLoginForm(data=request.POST)  # Initialize the form with POST data
        if form.is_valid():  # Validate the form
            user_role = form.cleaned_data['role']
            if user_role == 'teacher':
                is_teacher = True
            else:
                is_teacher = False
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])  # Authenticate the user
            if user is not None:  # Check if authentication was successful
                login(request, user)  # Log the user in
                if user.is_teacher is is_teacher:
                    if user_role == 'teacher':
                        return redirect('teacher_dashboard')
                    else:
                        return redirect('student_dashboard')
                else:

                    return render(request, 'accounts/login.html',
                              {'form': form, 'error': 'Insufficient authority!'})  # Return the form with errors
            else:
                return render(request, 'accounts/login.html',
                              {'form': form, 'error': 'User Not Exit!'})  # Return the form with errors
        else:
            print(form.errors)  # Print errors if the form is invalid
            return render(request, 'accounts/login.html', {'form': form, 'error_message': form.errors})  # Return the form with errors
    else:
        form = UserLoginForm()  # Initialize an empty form for GET requests
    return render(request, 'accounts/login.html', {'form': form})  # Display the login form

def register(request):
    if request.method == 'POST':  # Check if the form was submitted
        form = UserRegisterForm(request.POST)  # Initialize the form with POST data

        if form.is_valid():  # Validate the form
            user = form.save(commit=False)  # Save the form temporarily without committing to the database
            user.is_teacher = form.cleaned_data.get('is_teacher')  # Set the user's teacher status
            user.save()  # Finally save the user to the database
            return redirect('login')  # Redirect to login page after registration
        else:
            print(form.errors)  # Print errors if the form is invalid
    else:
        form = UserRegisterForm()  # Initialize an empty form for GET requests
    return render(request, 'accounts/register.html', {'form': form})  # Display the registration form

@login_required  # Decorator to ensure that the user is logged in
def teacher_dashboard(request):
    courses = Courses.objects.filter(teacher=request.user)  # Retrieve all courses taught by the logged-in teacher

    context = {
        'courses': courses,
    }

    return render(request, 'accounts/teacher_dashboard.html', context)  # Render the teacher dashboard with the courses

@login_required
def teacher_dashboard2(request):
    courses = Courses.objects.filter(teacher=request.user)  # Retrieve all courses taught by the logged-in teacher

    context = {
        'courses': courses,
    }

    return render(request, 'accounts/teacher_edit.html', context)  # Render the teacher dashboard with the courses


def logout(request):
    # Logout logic here
    return redirect('login')  # Redirect to the login page after logging out

@login_required  # Decorator to ensure that the user is logged in
def upload_guide(request):
    if request.method == 'POST':  # Check if the form was submitted
        uploaded_file = request.FILES['fileUpload']  # Access the uploaded file
        rubric_file = request.FILES.get('Rubric')  # Access the uploaded file
        course_id = request.POST['course_id']  # Get the course ID from the form

        fs = FileSystemStorage()  # Initialize file system storage
        name = fs.save(uploaded_file.name, uploaded_file)  # Save the uploaded file

        if name.endswith('.docx'):
            content = read_docx(os.path.join(BASE_DIR, 'media', name))  # Read .docx files using read_docx

        elif name.endswith('.cpp'):
            content = read_cpp_with_newlines(os.path.join(BASE_DIR, 'media', name))

        elif name.endswith('.pdf'):
            time.sleep(1)
            content = read_pdf(os.path.join(BASE_DIR, 'media', name))

        else:
            content = ''  # If file is neither .doc nor .docx, return empty string
        rubric_content = ''
        if rubric_file:
            rubric_file_name = fs.save(rubric_file.name, rubric_file)
            rubric_content = read_docx(os.path.join(BASE_DIR, 'media', rubric_file_name))

        course = Courses.objects.get(id=course_id)  # Retrieve the course based on ID
        content = 'guide content is: ' + content + ', rubric content is: ' + rubric_content + 'Improve the rubric according to the guide and rubric given with words described to each level as detailed as possible, should be strictly following given guide and/or rubric. If no rubric is given, creating a new rubric based on the guide.'  # Append additional text to the content

        response = get_response(content)  # Get a response based on the content
        course.guide = response  # Set the course guide to the response
        course.save()  # Save the updated course
        return redirect('teacher_dashboard')  # Redirect to the teacher dashboard
    else:
        return render(request, 'accounts/teacher_dashboard.html')  # Render the dashboard page for GET requests



def student_dashboard(request):
    selections = Selection.objects.filter(students=request.user)  # Retrieve all course selections for the logged-in student
    courses = [selection.course for selection in selections]  # Extract courses from selections
    context = {
        'courses': courses,
    }
    return render(request, 'accounts/student_dashboard.html', context)  # Render the student dashboard with the courses

def save_guide_changes(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Courses, pk=course_id)
        guide_content = request.POST.get('guide')
        course.guide = guide_content
        course.save()
        return redirect('teacher_dashboard')
    return HttpResponse("Invalid request", status=400)


def upload_homework(request):

    if request.method == 'POST':  # Check if the form was submitted
        uploaded_file = request.FILES['fileUpload']  # Access the uploaded file
        course_id = request.POST['course_id']  # Get the course ID from the form
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'media'))  # Initialize file system storage

        name = fs.save(uploaded_file.name, uploaded_file)  # Save the uploaded file

        if name.endswith('.docx'):
            content = read_docx(os.path.join(BASE_DIR, 'media', 'media', name))  # Read .docx files using read_docx
        elif name.endswith('.cpp'):
            content = read_cpp_with_newlines(os.path.join(BASE_DIR, 'media', 'media', name))

        elif name.endswith('.pdf'):

            content = read_pdf(os.path.join(BASE_DIR, 'media', 'media', name))

        else:
            content = ''  # If file is neither .doc nor .docx, return empty string
        course = Courses.objects.get(id=course_id)  # Retrieve the course based on ID
        homework = Selection.objects.get(course=course, students=request.user)
        content = 'guide is : ' + course.guide + ' student\'s homework is: ' + content + 'According to the above, please give me a detailed backward, provide advices for improvement, but never directly show a solution!'  # Append additional text to the content

        response = get_response(content)  # Get a response based on the content
        homework.backward = response  # Set the course guide to the response
        homework.save()  # Save the updated course
        return redirect('student_dashboard')  # Redirect to the teacher dashboard
    else:
        return render(request, 'accounts/student_dashboard.html')  # Render the dashboard page for GET requests


def homework(request):
    selections = Selection.objects.filter(
        students=request.user)  # Retrieve all course selections for the logged-in student
    courses = [selection.course for selection in selections]  # Extract courses from selections
    context = {
        'courses': courses,
        'selections': selections
    }
    return render(request, 'accounts/student_homework.html', context)  # Render the student dashboard with the courses

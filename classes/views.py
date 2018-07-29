from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Classroom, Student
from .forms import ClassroomForm, SigninForm, SignupForm, StudentForm
from django.contrib.auth import login, authenticate, logout


def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(user.password)
            user.save()

            login(request, user)
            return redirect("classroom-list")
    context = {
        "form": form,
    }
    return render(request, 'signup.html', context)


def signin(request):
    form = SigninForm()
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('classroom-list')
    context = {"form": form}
    return render(request, 'signin.html', context)


def signout(request):
    logout(request)
    return redirect("signin")


def classroom_list(request):
    classrooms = Classroom.objects.all()
    context = {
        "classrooms": classrooms,
    }
    return render(request, 'classroom_list.html', context)


def classroom_detail(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    all_student = Student.objects.all().order_by('name', 'exam_grade')
    context = {"classroom": classroom, "all_student": all_student}
    return render(request, 'classroom_detail.html', context)


def classroom_create(request):
    if request.user.is_anonymous:
        return redirect('signin')
    form = ClassroomForm()
    if request.method == "POST":
        form = ClassroomForm(request.POST, request.FILES or None)
        if form.is_valid():
            form = form.save(commit=False)
            form.teacher = request.user
            form.save()
            messages.success(request, "Successfully Created!")
            return redirect('classroom-list')
        print(form.errors)
    context = {
        "form": form,
    }
    return render(request, 'create_classroom.html', context)


def create_student(request):
    if request.user.is_anonymous:
        return redirect('signin')
    form = StudentForm()
    if request.method == "POST":
        print("test post ")
        form = StudentForm(request.POST, request.FILES or None)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            messages.success(request, "Successfully Created!")
            return redirect('classroom-list')
        print(form.errors)
    context = {
        "form": form,
    }
    return render(request, 'create_student.html', context)


def student_update(request, student_id):
    student = Student.objects.get(id=student_id)
    form = StudentForm(instance=student)
    if request.method == "POST":
        form = StudentForm(
            request.POST, request.FILES or None, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Edited!")
            return redirect('classroom-list')
        print(form.errors)
    context = {
        "form": form,
        "classroom": student,
    }
    return render(request, 'update_student.html', context)


def student_delete(request, student_id):
    Student.objects.get(id=student_id).delete()
    messages.success(request, "Successfully Deleted!")
    return redirect('classroom-list')


def classroom_update(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    form = ClassroomForm(instance=classroom)
    if request.method == "POST":
        form = ClassroomForm(
            request.POST, request.FILES or None, instance=classroom)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Edited!")
            return redirect('classroom-list')
        print(form.errors)
    context = {
        "form": form,
        "classroom": classroom,
    }
    return render(request, 'update_classroom.html', context)


def classroom_delete(request, classroom_id):
    Classroom.objects.get(id=classroom_id).delete()
    messages.success(request, "Successfully Deleted!")
    return redirect('classroom-list')


# def restaurant_create(request):
#     if request.user.is_anonymous:
#         return redirect('signin')
#     form = RestaurantForm()
#     if request.method == "POST":
#         form = RestaurantForm(request.POST, request.FILES)
#         if form.is_valid():
#             restaurant = form.save(commit=False)
#             restaurant.owner = request.user
#             restaurant.save()
#             return redirect('restaurant-list')
#     context = {
#         "form":form,
#     }
#     return render(request, 'create.html', context)
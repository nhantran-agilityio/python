from django.shortcuts import render
from rest_framework import viewsets
from .serializers import StudentSerializer

from django.views.generic import ListView
from .models import Student

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentListView(ListView):
    model = Student
    template_name = 'student_list.html'

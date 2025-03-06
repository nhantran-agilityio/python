from rest_framework import generics, permissions
from .models import Instructor
from .serializers import InstructorSerializer


class InstructorCreateView(generics.CreateAPIView):
    queryset = Instructor.objects.all().select_related('user')
    serializer_class = InstructorSerializer
    permission_classes = [permissions.IsAdminUser]


class InstructorUpdateView(generics.UpdateAPIView):
    queryset = Instructor.objects.all().select_related('user')
    serializer_class = InstructorSerializer
    permission_classes = [permissions.IsAdminUser]


class InstructorDeleteView(generics.DestroyAPIView):
    queryset = Instructor.objects.all().select_related('user')
    serializer_class = InstructorSerializer
    permission_classes = [permissions.IsAdminUser]

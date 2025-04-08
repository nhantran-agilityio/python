from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from apps.accounts.models import User


from .models import Financial
from .serializers import FinancialSerializer


class FinancialDetailAPIView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        financial = get_object_or_404(FinancialSerializer, user=user)
        serializer = FinancialSerializer(financial)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update financial details partially.",
        request_body=FinancialSerializer,
        responses={
            200: FinancialSerializer,
            400: "Invalid data provided."
        }
    )
    def patch(self, request, pk):
        financial = get_object_or_404(Financial, pk=pk)
        serializer = FinancialSerializer(financial, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

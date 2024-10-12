from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CustomerSerializer
from datetime import datetime

@api_view(['POST'])
def create_customer(request):
    if request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            birth_date = serializer.validated_data['dob']
            today = datetime.now().date()

            # Check if birth_date is in the future
            if birth_date > today:
                return JsonResponse({'error': 'Date of birth cannot be in the future.'},
                                    status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

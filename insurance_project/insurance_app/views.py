from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CustomerSerializer
from .models import Quote, Customer, Policy
from datetime import datetime, date

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


@api_view(['POST'])
def create_quote(request):
    customer_id = request.data.get('customer_id')
    type_ = request.data.get('type')

    try:
        # Fetch the customer and policy
        customer = Customer.objects.get(id=customer_id)
        policy = Policy.objects.get(type=type_)  # Get the corresponding policy type

        # Calculate age to determine premium and cover adjustments
        today = date.today()
        age = today.year - customer.dob.year - (
                    (today.month, today.day) < (customer.dob.month, customer.dob.day))

        # Calculate modified premium and cover based on age
        if age < 18:
            premium = policy.premium * 0.8  # 20% discount for underage
            cover = policy.cover * 0.8  # 20% less cover
        else:
            premium = policy.premium
            cover = policy.cover

    except (Customer.DoesNotExist, Policy.DoesNotExist):
        return Response({'error': 'Invalid customer or policy type.'}, status=status.HTTP_400_BAD_REQUEST)

    # Create the quote with the calculated premium and cover
    quote = Quote.objects.create(customer=customer, policy=policy, premium=premium, cover=cover)

    return Response({
        'quote_id': quote.id,
        'customer_id': quote.customer.id,
        'policy_id': quote.policy.id,
        'premium': str(quote.premium),
        'cover': str(quote.cover),
        'status': quote.status
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def accept_quote(request):
    quote_id = request.data.get('quote_id')
    status_param = request.data.get('status')

    # Check if the status parameter is provided
    if status_param != 'accepted':
        return Response({'error': 'Invalid status. Status must be "accepted".'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Retrieve the quote based on the provided quote_id
        quote = Quote.objects.get(id=quote_id)

        # Check the current status
        if quote.status == 'NEW':
            # Update the status to QUOTED
            quote.status = 'QUOTED'
            quote.save()  # This will trigger the creation of a new PolicyHistory record

            return Response({
                'quote_id': quote.id,
                'status': quote.status
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Quote cannot be accepted as it is not in NEW status.'
            }, status=status.HTTP_400_BAD_REQUEST)

    except Quote.DoesNotExist:
        return Response({'error': 'Quote not found.'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
def pay_quote(request):
    quote_id = request.data.get('quote_id')
    status_param = request.data.get('status')  # Get the status parameter

    # Check if the status parameter is provided
    if status_param != 'active':
        return Response({'error': 'Invalid status. Status must be "active".'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Retrieve the quote based on the provided quote_id
        quote = Quote.objects.get(id=quote_id)

        # Check the current status
        if quote.status == 'QUOTED':
            # Simulate payment processing here
            # payment_processing(quote)  # Uncomment this line when implementing actual payment logic

            # Update the status to LIVE
            quote.status = 'LIVE'
            quote.save()  # This will trigger the creation of a new PolicyHistory record

            return Response({
                'quote_id': quote.id,
                'status': quote.status
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Quote cannot be paid as it is not in QUOTED status.'
            }, status=status.HTTP_400_BAD_REQUEST)

    except Quote.DoesNotExist:
        return Response({'error': 'Quote not found.'}, status=status.HTTP_404_NOT_FOUND)


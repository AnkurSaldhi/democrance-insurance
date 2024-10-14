from rest_framework import serializers
from .models import Customer
from .constants import FUTURE_DOB_ERROR
from datetime import date


class CustomerSerializer(serializers.ModelSerializer):
    # Override dob to accept and return the date in DD-MM-YYYY format
    dob = serializers.DateField(
        input_formats=['%d-%m-%Y'],  # Accept DD-MM-YYYY format
        format='%d-%m-%Y'  # Return DD-MM-YYYY format in response
    )

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'dob', 'email', 'created_at', 'updated_at']

    def validate_dob(self, value):
        if value > date.today():
            raise serializers.ValidationError(FUTURE_DOB_ERROR)
        return value

    def validate_email(self, value):
        """Check if the email is already in use"""
        email = value.lower()  # Convert email to lowercase for case-insensitive check

        # Check if a customer with this email (case-insensitive) already exists, doing iexact for addition security
        if Customer.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("Email already exists.")

        return email

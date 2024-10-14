```markdown
# Insurance Management API

## Overview

This application provides an API for managing customers, policies, and quotes in an insurance management system. It allows users to create/search customers, create and accept quotes, manage policy details, and track the history of policy statuses.

## Models

### 1. Customer

- **Fields**:
  - `first_name`: The first name of the customer.
  - `last_name`: The last name of the customer.
  - `dob`: The date of birth of the customer (stored as `YYYY-MM-DD` but expected in `DD-MM-YYYY` format).
  - `email`: Unique email address for the customer.
  - `created_at`: Timestamp when the customer record was created.
  - `updated_at`: Timestamp for the last update of the customer record.

### 2. Policy - Seed data created using migration (please check migrations/0003_add_policies_with_premium_cover.py)

- **Fields**:
  - `name`: The name of the insurance policy.
  - `type`: The type of insurance policy (data added using seed migration e.g., personal-accident, health-insurance).
  - `premium`: Default/Base premium amount for the policy.
  - `cover`: Default/Base coverage amount for the policy.
  - `created_at`: Timestamp when the policy record was created.
  - `updated_at`: Timestamp for the last update of the policy record.

### 3. Quote

- **Fields**:
  - `customer`: Foreign key linking to the Customer model.
  - `policy`: Foreign key linking to the Policy model.
  - `status`: The current status of the quote (e.g., NEW, QUOTED, LIVE).
  - `premium`: Calculated premium based on age.
  - `cover`: Calculated coverage based on age.
  - `buy_date`: Date when the policy is purchased.
  - `expiry`: Expiry date of the policy.
  - `created_at`: Timestamp when the quote was created.
  - `updated_at`: Timestamp for the last update of the quote record.

### 4. PolicyHistory - These objects get created upon quote's status changes, logic added in Quote model's save() method.

- **Fields**:
  - `quote`: Foreign key linking to the Quote model.
  - `last_status`: The status of the quote at the time of history creation.
  - `changed_at`: Timestamp when the status was changed.

## Constants

- **POLICY_STATUS_CHOICES**: Contains possible statuses for quotes (e.g., NEW, QUOTED, LIVE).
- **INSURANCE_TYPES**: Contains different types of insurance policies.
- **Error Messages**: Constants for different error messages to maintain consistency across the application.
```

## API Endpoints


### 1. Create Customer
- **URL**: `/api/v1/create_customer/`
- **Method**: POST
- **Description**: Creates a new customer with unique email.
- **Payload**: 
  ```json
  {
      "first_name": "Test",
      "last_name": "User",
      "dob": "25-12-1990",
      "email": "test.user@gmail.com"
  }
  ```

### 2. Create Quote
- **URL**: `/api/v1/create_quote/`
- **Method**: POST
- **Description**: Creates a new quote based on customer and policy type.
- **Payload**: 
  ```json
  {
      "customer_id": 1,
      "type": "personal-accident"
  }
  ```
  
### 3. Accept Quote
- **URL**: `/api/v1/accept_quote/`
- **Method**: POST
- **Description**: Accepts a quote and changes its status to QUOTED. Also, PolicyHistory object gets created here.
- **Payload**: 
  ```json
  {
      "quote_id": 1,
      "status": "accepted"
  }
  ```

### 4. Pay Quote
- **URL**: `/api/v1/pay_quote/`
- **Method**: POST
- **Description**: Processes payment for a quote and sets its status to LIVE.
- **Payload**: 
  ```json
  {
      "quote_id": 1,
      "status": "active"
  }
  ```

### 5. Get Customer Policies
- **URL**: `/api/v1/policies/?customer_id=1`
- **Method**: GET
- **Description**: Retrieves all policies associated with a specific customer with status, type etc.
- **Query Parameters**: 
  - `customer_id`: ID of the customer.

### 6. Get Policy Details
- **URL**: `/api/v1/policies/<quote_id>/`
- **Method**: GET
- **Description**: Retrieves details of a specific quote/policy.
- **Flow**: 
  - Retrieve the quote based on the provided ID.
  - Prepare and return policy details including status, premium, cover, buy date, and expiry date.

### 7. Get Policy History
- **URL**: `/api/v1/policies/<quote_id>/history/`
- **Method**: GET
- **Description**: Retrieves the history of status changes for a specific quote/policy.
- **Flow**: 
  - Retrieve the quote to ensure it exists.
  - Query all policy history records associated with the quote, ordered by changed_at.

### 8. Search Customers
- **URL**: `/api/v1/search_customers/`
- **Method**: GET
- **Description**: Searches for customers based on name or dob or policy_type.
- **Query Parameters (One of these)**: 
  - `name`: Customer's name (first or last).
  - `dob`: Customer's date of birth (DD-MM-YYYY).
  - `policy_type`: Customer's with this policy type having quotes created
- **Flow**: 
  - Filter customers based on the provided name or dob or policy_type.
  - Return the serialized customer data.
  - Then clicking on one of these customers, frontend can hit "List Policies" api for a customer by passing customer_id



## We should choose the "Same Authentication System" because:

Implementing the same authentication system for both insurance company users and customers(assuming 2 user types for now) offers several key advantages. 
- It simplifies management by providing a single point of user authentication, which reduces complexity in code and configuration. This consistency improves the user experience, as both user types will have a uniform interface for logging in, resetting passwords, and managing their accounts. 
- Using a role-based access control approach within a unified system allows for easier implementation of permissions used for different user needs. This means administrators can manage user roles and permissions from one central location, streamlining user management tasks. 
- Maintaining a single authentication system enhances security by minimizing potential vulnerabilities associated with multiple systems, making it easier to implement best practices for user data protection.

### Code Explanation

Below "sample code" shows how to use the same authentication system in Django, focusing on role-based access control and user management.

#### 1. **Models**

We can use Django's built-in `User` model and extend it with a custom user type, sample code below:

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('insurance_user', 'Insurance Company User'),
        ('customer', 'Customer'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
```

#### 2. **Views**

The login view can handle both user types seamlessly, sample code below:

```python
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        # Redirect based on user type
        if user.user_type == 'insurance_user':
            return JsonResponse({'message': 'Welcome, Insurance User!'})
        else:
            return JsonResponse({'message': 'Welcome, Customer!'})
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)
```

#### 3. **Permissions**

Using Django's permission system to manage access levels, sample code below:

```python
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('insurance_app.view_policy', raise_exception=True)
def view_policy(request):
    # Logic for viewing policies
    pass
```

### Conclusion for same authentication:

This approach allows both insurance company users and customers to authenticate through a single, unified system while ensuring security and providing a consistent user experience. The ability to implement role-based access control makes it easy to customize permissions according to user needs, further enhancing the system's flexibility and maintainability.


# Project Setup:
- Clone the Repository and navigate to insurance_project folder
- Create a virtual environment
  - `python3 -m venv env_name`
- Activate the virtual environment (Mac)
  - `source env_name/bin/activate`
- Install dependencies
  - `pip3 install -r requirements.txt`
- Run migrations (It will create 5 seed policies with default cover and premium, see 0003_add_policies_with_premium_cover.py)
  - `python3 manage.py migrate`
- Run django server
  - `python3 manage.py runserver`




# Curl Requests:

```bash
# create customer

curl -X POST http://localhost:8000/api/v1/create_customer/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "dob": "21-10-1994",
    "email": "test.user@example.com"
}'


# create quote
curl -X POST http://localhost:8000/api/v1/create_quote/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "type": "personal-accident" 
}'


#accept quote
curl -X POST http://localhost:8000/api/v1/accept_quote/ \
  -H "Content-Type: application/json" \
  -d '{
    "quote_id": 1,
    "status": "accepted"
}'



#pay quote
curl -X POST http://localhost:8000/api/v1/pay_quote/ \
  -H "Content-Type: application/json" \
  -d '{
    "quote_id": 1,
    "status": "active"
}'



# list policies
curl -X GET "http://localhost:8000/api/v1/policies/?customer_id=1"


# policy details
curl -X GET http://localhost:8000/api/v1/policies/1/


# policy history
curl -X GET http://localhost:8000/api/v1/policies/1/history/


# search customer
curl -X GET "http://localhost:8000/api/v1/search_customers/?name=Test"
curl -X GET "http://localhost:8000/api/v1/search_customers/?dob=21-10-2014"
curl -X GET "http://localhost:8000/api/v1/search_customers/?policy_type=health-insurance"
```
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User  # Assuming you are using Django's built-in User model
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@api_view(['POST'])
def CreateUserView(request):
    data = request.data
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')
    password = data.get('password')

    # Validate input data (this is crucial to prevent errors and ensure data integrity)
    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Check if the user already exists based on email
        if User.objects.filter(email=email).exists():
            return Response({'error': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        user = User.objects.create_user(username=email, email=email, password=password)

        # Optionally, set additional fields if provided
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name

        user.save()

        # Optionally, perform additional tasks like sending confirmation email
        print("User created successfully!")
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def LoginUserView(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')
    user = authenticate(username=email, password=password)
    if user is not None:
        login(request, user)
        print("Login Successfully!")
        return Response({'message': 'Login Successfully'}, status=status.HTTP_201_CREATED)
    else:
         return Response({'error': 'Login Password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)




@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful!'})

@login_required
def check_auth_view(request):
    return JsonResponse({'username': request.user.username})
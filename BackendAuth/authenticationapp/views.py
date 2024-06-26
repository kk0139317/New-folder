from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User  # Assuming you are using Django's built-in User model
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from .models import ImageGeneration, GeneratedImage
from rest_framework.permissions import IsAuthenticated
import os
from django.conf import settings
from django.utils import timezone
import random
from PIL import Image, ImageDraw
import json
from rest_framework.decorators import api_view, permission_classes


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

# @api_view(['POST'])
# def LoginUserView(request):
#     data = request.data
#     email = data.get('email')
#     password = data.get('password')
#     user = authenticate(username=email, password=password)
#     if user is not None:
#         login(request, user)
#         print("Login Successfully!")
#         return Response({'message': 'Login Successfully'}, status=status.HTTP_201_CREATED)
#     else:
#          return Response({'error': 'Login Password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def LoginUserView(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')
    user = authenticate(username=email, password=password)
    if user is not None:
        login(request, user)
        refresh = RefreshToken.for_user(user)
        return Response({
            'token': str(refresh.access_token),
            'username': user.username,
            'message': 'Login Successfully'
        }, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Email or password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful!'})

@login_required
def check_auth_view(request):
    return JsonResponse({'username': request.user.username})



# Image Generation 

def create_sample_image(prompt, num_images, folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    images = []
    for i in range(num_images):
        img = Image.new('RGB', (300, 300), color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        d = ImageDraw.Draw(img)
        d.text((10,10), f"{prompt} {i+1}", fill=(255,255,255))
        img_path = os.path.join(folder_name, f"{prompt}_{i+1}.png")
        img.save(img_path)
        images.append(img_path)
    return images

@csrf_exempt
def generate_images(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        prompt = data.get('prompt')
        num_images = int(data.get('numImages'))
        username = data.get('username')

        user = User.objects.get(username=username)  # Get the user from the database

        generation = ImageGeneration.objects.create(
            user=user,
            prompt=prompt,
            num_images=num_images,
            created_at=timezone.now()
        )

        folder_names = [os.path.join(settings.MEDIA_ROOT, f"{prompt}_set_{i+1}") for i in range(5)]
        all_images = []

        for folder in folder_names:
            images = create_sample_image(prompt, num_images, folder)
            for img_path in images:
                image_instance = GeneratedImage.objects.create(generation=generation, image=img_path)
                all_images.append({
                    'url': image_instance.image.url,
                    'prompt': prompt,
                    'folder': folder
                })

        return JsonResponse({'images': all_images})
    

@api_view(['GET'])
def get_user_prompts(request, username):
    user = User.objects.get(username=username)
    prompts = ImageGeneration.objects.filter(user=user).values('id','prompt', 'num_images')  # Query all prompts and select specific fields
    for prompt in prompts:
        prompt['prompt'] = ' '.join(prompt['prompt'].split()[:3]) + ' ...'
    
    return JsonResponse(list(prompts), safe=False)




def fetch_images(request):
    if request.method == 'GET':
        prompt = request.GET.get('prompt')
        generations = ImageGeneration.objects.filter(id=prompt)
        all_images = []

        for generation in generations:
            images = GeneratedImage.objects.filter(generation=generation)
            for image in images:
                all_images.append({
                    'id': image.id,
                    'url': image.image.url,
                    'prompt': generation.prompt,
                })

        return JsonResponse({'images': all_images})
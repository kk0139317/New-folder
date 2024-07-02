from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserImageGeneration, UserGeneratedImage, UserSubPrompt, UserMasterPrompt, ProfileDetail
from rest_framework.permissions import IsAuthenticated
import os
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.utils import timezone
import random
from PIL import Image, ImageDraw
import json
import logging
from .utils import create_sample_image

logger = logging.getLogger(__name__)

@api_view(['POST'])
def CreateUserView(request):
    data = request.data
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        if User.objects.filter(email=email).exists():
            return Response({'error': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=email, email=email, password=password)
        profile = ProfileDetail(username=email, email=email, credit=20, name=name)
        profile.save()
        
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name

        user.save()
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

# def create_sample_image(prompt, num_images, folder_name):
#     if not os.path.exists(folder_name):
#         os.makedirs(folder_name)
#     images = []
#     for i in range(num_images):
#         img = Image.new('RGB', (300, 300), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
#         d = ImageDraw.Draw(img)
#         d.text((10, 10), f"{prompt} {i+1}", fill=(255, 255, 255))
#         img_path = os.path.join(folder_name, f"{prompt}_{i+1}.png")
#         img.save(img_path)
#         images.append(img_path)
#     return images

@csrf_exempt
def generate_images(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        prompts = data.get('prompt')
        num_images = int(data.get('numImages'))
        username = data.get('username')
        profile = ProfileDetail.objects.get(username=username)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        prompt_list = [prompt.strip() for prompt in prompts.split(',')]
        master_prompt = UserMasterPrompt.objects.create(user=user, created_at=timezone.now(), prompt=prompts)
        all_images = []

        for prompt in prompt_list:
            sub_prompt = UserSubPrompt.objects.create(master_prompt=master_prompt, prompt_text=prompt)

            for i in range(1):
                generation = UserImageGeneration.objects.create(
                    sub_prompt=sub_prompt,
                    num_images=num_images,
                    created_at=timezone.now()
                )

                folder = os.path.join(settings.MEDIA_ROOT, f"{master_prompt.unique_id}/{prompt.replace(' ', '_')}")
                location = os.path.join(settings.MEDIA_URL, f"{master_prompt.unique_id}/{prompt.replace(' ', '_')}")
                images = create_sample_image(prompt, num_images, folder, location)

                
                for img_path in images:
                    # Log the length of the image path
                    logger.info(f'Image path length: {len(img_path)}')
                    if len(img_path) > 1024:
                        logger.warning(f'Image path exceeds 1024 characters: {img_path}')
                    
                    image_instance = UserGeneratedImage.objects.create(generation=generation, image_path=img_path)
                    profile.credit -= 0.25
                    profile.save()
                    all_images.append({
                        'id': image_instance.id,
                        'url': image_instance.image_path,
                        'sub_prompt_id': sub_prompt.id,
                        'sub_prompt_text': sub_prompt.prompt_text,
                        'num_images': generation.num_images,
                        'created_at': generation.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    })

        return JsonResponse({'images': all_images})

    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def get_user_prompts(request, username):
    if request.method == 'GET':
        master_prompts = UserMasterPrompt.objects.filter(user__username=username).order_by('-created_at').values(
            'id', 'unique_id', 'created_at', 'prompt'
        )
        data = []
        for master_prompt in master_prompts:
            sub_prompts = UserSubPrompt.objects.filter(master_prompt_id=master_prompt['id']).values('id', 'prompt_text')
            master_prompt_data = {
                'id': master_prompt['id'],
                'unique_id': master_prompt['unique_id'],
                'master_prompt': master_prompt['prompt'],
                'created_at': master_prompt['created_at'],
                'sub_prompts': list(sub_prompts)
            }
            data.append(master_prompt_data)
        return JsonResponse(data, safe=False)

def fetch_images(request):
    if request.method == 'GET':
        master_prompt_id = request.GET.get('prompt')
        try:
            master_prompt = UserMasterPrompt.objects.get(id=master_prompt_id)
        except UserMasterPrompt.DoesNotExist:
            return JsonResponse({'error': 'Master prompt not found'}, status=404)
        
        sub_prompts = master_prompt.subprompts.all()
        all_images = []

        for sub_prompt in sub_prompts:
            generations = UserImageGeneration.objects.filter(sub_prompt=sub_prompt)
            for generation in generations:
                images = generation.images.all()
                for image in images:
                    all_images.append({
                        'id': image.id,
                        'url': image.image_path,
                        'sub_prompt_id': sub_prompt.id,
                        'sub_prompt_text': sub_prompt.prompt_text,
                        'num_images': generation.num_images,
                        'created_at': generation.created_at,
                    })

        return JsonResponse({'images': all_images})


@csrf_exempt
def get_profile(request, username):
    if request.method == 'GET':
        try:
            profile = ProfileDetail.objects.get(username=username)
            profile_data = {
                'credit': profile.credit,
                'name': profile.name,
                'email': profile.email,
                'username': profile.username,
                'photo': profile.image.url if profile.image else None  # Assuming image is a FileField/ImageField
            }
            return JsonResponse(profile_data)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Profile not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)
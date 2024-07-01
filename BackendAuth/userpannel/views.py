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
from .models import UserImageGeneration, UserGeneratedImage, UserSubPrompt, UserMasterPrompt
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

# @csrf_exempt
# def generate_images(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         prompts = data.get('prompts')
#         num_images = int(data.get('numImages'))
#         username = data.get('username')

#         user = User.objects.get(username=username)  # Get the user from the database
#         prompt_list = prompts.split(',')

#         all_images = []

#         for prompt in prompt_list:
#             prompt = prompt.strip()  # Clean any extra whitespace
#             generation = ImageGeneration.objects.create(
#                 user=user,
#                 prompt=prompt,
#                 num_images=num_images,
#                 created_at=timezone.now()
#             )

#             base_folder_name = os.path.join(settings.MEDIA_ROOT, f"master_prompt_{username}", prompt.replace(' ', '_'))

#             for i in range(5):
#                 folder = os.path.join(base_folder_name, f"scenario_{i+1}")
#                 images = create_sample_image(prompt, num_images, folder)
#                 for img_path in images:
#                     image_instance = GeneratedImage.objects.create(generation=generation, image=img_path)
#                     all_images.append({
#                         'url': image_instance.image.url,
#                         'prompt': prompt,
#                         'scenario': i + 1
#                     })

#         return JsonResponse({'images': all_images})
    

def create_sample_image(prompt, num_images, folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    images = []
    for i in range(num_images):
        img = Image.new('RGB', (300, 300), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        d = ImageDraw.Draw(img)
        d.text((10, 10), f"{prompt} {i+1}", fill=(255, 255, 255))
        img_path = os.path.join(folder_name, f"{prompt}_{i+1}.png")
        img.save(img_path)
        images.append(img_path)
    return images

# @csrf_exempt
# def generate_images(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         print('The data is',data)
#         prompts = data.get('prompt')
#         num_images = int(data.get('numImages'))
#         username = data.get('username')
#         print(prompts, num_images, username)
#         user = User.objects.get(username=username)
#         prompt_list = [prompt.strip() for prompt in prompts.split(',')]

#         master_prompt = UserMasterPrompt.objects.create(user=user, created_at=timezone.now())

#         all_images = []

#         for prompt in prompt_list:
#             sub_prompt = UserSubPrompt.objects.create(master_prompt=master_prompt, prompt_text=prompt)

#             for i in range(5):
#                 generation = UserImageGeneration.objects.create(
#                     sub_prompt=sub_prompt,
#                     num_images=num_images,
#                     created_at=timezone.now()
#                 )

#                 folder = os.path.join(settings.MEDIA_ROOT, f"{master_prompt.unique_id}/{prompt.replace(' ', '_')}/scenario_{i+1}")
#                 images = create_sample_image(prompt, num_images, folder)
#                 for img_path in images:
#                     image_instance = UserGeneratedImage.objects.create(generation=generation, image=img_path)
#                     all_images.append({
#                         'url': image_instance.image.url,
#                         'prompt': prompt,
#                         'scenario': i + 1
#                     })

#         return JsonResponse({'images': all_images})


@csrf_exempt
def generate_images(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        prompts = data.get('prompt')
        num_images = int(data.get('numImages'))
        username = data.get('username')
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        prompt_list = [prompt.strip() for prompt in prompts.split(',')]
        master_prompt = UserMasterPrompt.objects.create(user=user, created_at=timezone.now())
        all_images = []

        for prompt in prompt_list:
            sub_prompt = UserSubPrompt.objects.create(master_prompt=master_prompt, prompt_text=prompt)

            for i in range(1):
                generation = UserImageGeneration.objects.create(
                    sub_prompt=sub_prompt,
                    num_images=num_images,
                    created_at=timezone.now()
                )

                folder = os.path.join(settings.MEDIA_ROOT, f"{master_prompt.unique_id}/{prompt.replace(' ', '_')}/scenario_{i+1}")
                images = create_sample_image(prompt, num_images, folder)
                
                for img_path in images:
                    image_instance = UserGeneratedImage.objects.create(generation=generation, image=img_path)
                    all_images.append({
                        'id': image_instance.id,  # Assuming you want the ID of the generated image instance
                        'url': image_instance.image.url,
                        'sub_prompt_id': sub_prompt.id,
                        'sub_prompt_text': sub_prompt.prompt_text,
                        'num_images': generation.num_images,
                        'created_at': generation.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # Format datetime as string
                    })

        return JsonResponse({'images': all_images})

    return JsonResponse({'error': 'Invalid method'}, status=405)

# @api_view(['GET'])
# def get_user_prompts(request, username):
#     user = User.objects.get(username=username)
#     prompts = UserImageGeneration.objects.filter(user=user).values('id','prompt', 'num_images', 'created_at').order_by('-created_at')  # Query all prompts and select specific fields
#     for prompt in prompts:
#         prompt['prompt'] = ' '.join(prompt['prompt'].split()[:3]) + ' ...'
    
#     return JsonResponse(list(prompts), safe=False)


@csrf_exempt
def get_user_prompts(request, username):
    if request.method == 'GET':
        master_prompts = UserMasterPrompt.objects.filter(user__username=username).order_by('-created_at').values(
            'id', 'unique_id', 'created_at'
        )
        data = []
        for master_prompt in master_prompts:
            sub_prompts = UserSubPrompt.objects.filter(master_prompt_id=master_prompt['id']).values('id', 'prompt_text')
            master_prompt_data = {
                'id': master_prompt['id'],
                'unique_id': master_prompt['unique_id'],
                'created_at': master_prompt['created_at'],
                'sub_prompts': list(sub_prompts)
            }
            data.append(master_prompt_data)
        
        return JsonResponse(data, safe=False)


# def fetch_images(request):
#     if request.method == 'GET':
#         prompt = request.GET.get('prompt')
#         generations = UserImageGeneration.objects.filter(id=prompt)
#         all_images = []

#         for generation in generations:
#             images = UserGeneratedImage.objects.filter(generation=generation)
#             for image in images:
#                 all_images.append({
#                     'id': image.id,
#                     'url': image.image.url,
#                     'prompt': generation.prompt,
#                 })

#         return JsonResponse({'images': all_images})



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
                        'url': image.image.url,
                        'sub_prompt_id': sub_prompt.id,
                        'sub_prompt_text': sub_prompt.prompt_text,
                        'num_images': generation.num_images,
                        'created_at': generation.created_at,
                    })

        return JsonResponse({'images': all_images})
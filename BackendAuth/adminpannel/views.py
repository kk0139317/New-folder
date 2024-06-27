from django.shortcuts import render
from userpannel.models import UserImageGeneration, UserGeneratedImage, UserMasterPrompt, UserSubPrompt
from django.contrib.auth.models import User
# Create your views here.
# import os
# import random
# import json
# from PIL import Image, ImageDraw
# from django.conf import settings
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.utils import timezone
# from django.contrib.auth.models import User
# from .models import MasterPrompt, SubPrompt, ImageGeneration, GeneratedImage

def Index(request):
    data = UserMasterPrompt.objects.all().values('id', 'prompt', 'num_images', 'created_at', 'user__username').order_by('-created_at')  # Use 'user__username' to get the username
    for prompt in data:
        prompt['prompt'] = ' '.join(prompt['prompt'].split()[:3]) + ' ...'

    return render(request, 'admin/index.html', {'data':data})

def Images(request, pid):
    generations = UserImageGeneration.objects.filter(id=pid)
    all_images = []

    for generation in generations:
        images = UserGeneratedImage.objects.filter(generation=generation)
        for image in images:
            all_images.append({
                'id': image.id,
                'url': image.image.url,
                'prompt': generation.prompt,
            })

    return render(request, 'admin/images.html', {'generations': all_images})  # Pass the prompt ID to the image





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

#         user = User.objects.get(username=username)
#         prompt_list = [prompt.strip() for prompt in prompts.split(',')]

#         master_prompt = MasterPrompt.objects.create(user=user, created_at=timezone.now())

#         all_images = []

#         for prompt in prompt_list:
#             sub_prompt = SubPrompt.objects.create(master_prompt=master_prompt, prompt_text=prompt)

#             for i in range(5):
#                 generation = ImageGeneration.objects.create(
#                     sub_prompt=sub_prompt,
#                     num_images=num_images,
#                     created_at=timezone.now()
#                 )

#                 folder = os.path.join(settings.MEDIA_ROOT, f"{master_prompt.unique_id}/{prompt.replace(' ', '_')}/scenario_{i+1}")
#                 images = create_sample_image(prompt, num_images, folder)
#                 for img_path in images:
#                     image_instance = GeneratedImage.objects.create(generation=generation, image=img_path)
#                     all_images.append({
#                         'url': image_instance.image.url,
#                         'prompt': prompt,
#                         'scenario': i + 1
#                     })

#         return JsonResponse({'images': all_images})
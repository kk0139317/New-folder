import uuid
from django.db import models
from django.contrib.auth.models import User
from .utils import create_sample_image  # Assuming you have a utility function

class UserMasterPrompt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    prompt = models.TextField(max_length=1500)  # Changed to TextField for longer text
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.unique_id)

class UserSubPrompt(models.Model):
    master_prompt = models.ForeignKey(UserMasterPrompt, on_delete=models.CASCADE, related_name='subprompts')
    prompt_text = models.TextField(max_length=1500)

    def __str__(self):
        return self.prompt_text

class UserImageGeneration(models.Model):
    sub_prompt = models.ForeignKey(UserSubPrompt, on_delete=models.CASCADE, related_name='generations')
    num_images = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)



class UserGeneratedImage(models.Model):
    generation = models.ForeignKey('UserImageGeneration', on_delete=models.CASCADE, related_name='images')
    image_path = models.TextField()  # Store image paths as comma-separated string

    # def save(self, *args, **kwargs):
    #     if not self.pk:  # Check if this is a new instance
    #         # Generate sample images and get their paths
    #         image_paths = create_sample_image(self.generation.sub_prompt.prompt_text, self.generation.num_images, self.get_image_folder_path())
    #         self.image_path = ', '.join(image_paths)  # Store paths as comma-separated string
    #     super().save(*args, **kwargs)

    # def get_image_folder_path(self):
    #     return f"/media/{self.generation.sub_prompt.master_prompt.unique_id}/{self.generation.sub_prompt.prompt_text.replace(' ', '_')}"



# class UserGeneratedImage(models.Model):
#     generation = models.ForeignKey('UserImageGeneration', on_delete=models.CASCADE, related_name='images')
#     image_path = models.TextField()  # Store image paths as comma-separated string

#     def save(self, *args, **kwargs):
#         if not self.pk:  # Check if this is a new instance
#             # Generate sample images and get their paths
#             image_paths = create_sample_image(self.generation.sub_prompt.prompt_text, self.generation.num_images, self.get_image_folder_path())
#             self.image_path = ', '.join(image_paths)  # Store paths as comma-separated string
#         super().save(*args, **kwargs)

#     def get_image_folder_path(self):
#         return f"/media/{self.generation.sub_prompt.master_prompt.unique_id}/{self.generation.sub_prompt.prompt_text.replace(' ', '_')}"


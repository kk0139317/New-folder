import uuid
from django.db import models
from django.contrib.auth.models import User

class UserMasterPrompt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.unique_id)

class UserSubPrompt(models.Model):
    master_prompt = models.ForeignKey(UserMasterPrompt, on_delete=models.CASCADE, related_name='subprompts')
    prompt_text = models.CharField(max_length=255)

    def __str__(self):
        return self.prompt_text

class UserImageGeneration(models.Model):
    sub_prompt = models.ForeignKey(UserSubPrompt, on_delete=models.CASCADE, related_name='generations')
    num_images = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class UserGeneratedImage(models.Model):
    generation = models.ForeignKey(UserImageGeneration, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='generated_images/')

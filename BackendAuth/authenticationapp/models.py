import uuid
from django.db import models
from django.contrib.auth.models import User

class MasterPrompt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.unique_id)

class SubPrompt(models.Model):
    master_prompt = models.ForeignKey(MasterPrompt, on_delete=models.CASCADE, related_name='subprompts')
    prompt_text = models.CharField(max_length=255)

    def __str__(self):
        return self.prompt_text

class ImageGeneration(models.Model):
    sub_prompt = models.ForeignKey(SubPrompt, on_delete=models.CASCADE, related_name='generations')
    num_images = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class GeneratedImage(models.Model):
    generation = models.ForeignKey(ImageGeneration, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='generated_images/')

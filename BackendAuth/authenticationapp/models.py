from django.db import models
from django.contrib.auth.models import User

class ImageGeneration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.CharField(max_length=255)
    num_images = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.prompt

class GeneratedImage(models.Model):
    generation = models.ForeignKey(ImageGeneration, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='generated_images/')

# Generated by Django 5.0.6 on 2024-06-27 04:46

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageGeneration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_images', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='GeneratedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='generated_images/')),
                ('generation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='authenticationapp.imagegeneration')),
            ],
        ),
        migrations.CreateModel(
            name='MasterPrompt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubPrompt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt_text', models.CharField(max_length=255)),
                ('master_prompt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subprompts', to='authenticationapp.masterprompt')),
            ],
        ),
        migrations.AddField(
            model_name='imagegeneration',
            name='sub_prompt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='generations', to='authenticationapp.subprompt'),
        ),
    ]

# Generated by Django 4.2.3 on 2023-08-06 20:36

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import websiteProject.web.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, validators=[websiteProject.web.validators.TextAndNumsOnlyValidator])),
                ('author', models.CharField(max_length=30)),
                ('genre', models.CharField(choices=[('FAN', 'Fantasy'), ('SCIF', 'Sci-Fi'), ('NFAN', 'Nonfiction')], max_length=255)),
                ('synopsis', models.TextField(blank=True, null=True)),
                ('cover_url', models.URLField()),
                ('book', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, unique=True, validators=[django.core.validators.MinLengthValidator(2), websiteProject.web.validators.TextAndNumsOnlyValidator])),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(6), websiteProject.web.validators.TextAndNumsOnlyValidator])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
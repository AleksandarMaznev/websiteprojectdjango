# Generated by Django 4.2.3 on 2023-08-09 22:49

from django.db import migrations, models
import websiteProject.web.custom_upload_files


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_remove_book_book_book_book_file_alter_book_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_file',
            field=models.FileField(upload_to=websiteProject.web.custom_upload_files.upload_file),
        ),
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.FileField(upload_to=websiteProject.web.custom_upload_files.upload_file),
        ),
    ]

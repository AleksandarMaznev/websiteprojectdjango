# Generated by Django 4.2.3 on 2023-08-09 08:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_alter_book_book_alter_book_cover_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='cover_url',
            new_name='cover',
        ),
    ]

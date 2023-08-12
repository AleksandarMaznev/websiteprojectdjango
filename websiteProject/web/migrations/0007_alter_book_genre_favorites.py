# Generated by Django 4.2.3 on 2023-08-11 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_alter_book_book_file_alter_book_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.CharField(choices=[('Fantasy', 'Fantasy'), ('Sci-Fi', 'Sci-Fi'), ('Nonfiction', 'Nonfiction'), ('Mystery', 'Mystery'), ('Thriller', 'Thriller'), ('Romance', 'Romance'), ('Historical Fiction', 'Historical Fiction'), ('Adventure', 'Adventure'), ('Horror', 'Horror'), ('Drama', 'Drama'), ('Comedy', 'Comedy'), ('Biography', 'Biography'), ('Self-Help', 'Self-Help'), ('Science', 'Science'), ('Poetry', 'Poetry')], max_length=255),
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorited_on', models.DateTimeField(blank=True, null=True)),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.book')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.profile')),
            ],
        ),
    ]
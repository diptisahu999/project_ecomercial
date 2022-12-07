# Generated by Django 4.1.3 on 2022-11-25 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('mobile', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=15)),
                ('address', models.TextField(blank=True, max_length=200, null=True)),
                ('pic', models.FileField(default='sad.png', upload_to='profile')),
                ('dob', models.DateTimeField(blank=True, null=True)),
                ('gender', models.CharField(max_length=30)),
            ],
        ),
    ]
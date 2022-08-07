# Generated by Django 4.0.6 on 2022-07-30 06:30

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('alternate1_contact', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('alternate2_contact', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('email', models.CharField(blank=True, max_length=300, null=True)),
                ('about_us', models.TextField(blank=True, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos/')),
                ('instagram_link', models.CharField(blank=True, max_length=500, null=True)),
                ('facebook_link', models.CharField(blank=True, max_length=500, null=True)),
                ('twitter_link', models.CharField(blank=True, max_length=500, null=True)),
                ('youtube_link', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Homepage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=300, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Homepage_Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='homepage_image/')),
                ('sorting_number', models.PositiveBigIntegerField(blank=True, null=True)),
                ('homepage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='home.homepage')),
            ],
        ),
        migrations.CreateModel(
            name='Founder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_head', models.BooleanField(default=False)),
                ('detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='founders', to='home.founder')),
            ],
        ),
    ]
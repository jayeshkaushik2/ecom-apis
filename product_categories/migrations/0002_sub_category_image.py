# Generated by Django 4.0.6 on 2022-07-24 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_categories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sub_category',
            name='image',
            field=models.ImageField(default='', upload_to='sub_categories/'),
            preserve_default=False,
        ),
    ]
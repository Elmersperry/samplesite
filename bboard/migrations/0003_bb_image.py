# Generated by Django 5.2 on 2025-04-16 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0002_rubric_alter_bb_options_alter_bb_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bb',
            name='image',
            field=models.ImageField(null=True, upload_to='postings/', verbose_name='Изображение'),
        ),
    ]

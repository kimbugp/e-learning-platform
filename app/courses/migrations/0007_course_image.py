# Generated by Django 2.2.3 on 2019-07-26 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_course_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='image',
            field=models.URLField(blank=True, verbose_name='course_image'),
        ),
    ]

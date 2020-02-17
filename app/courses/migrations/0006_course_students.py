# Generated by Django 2.2.3 on 2019-07-25 11:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("courses", "0005_auto_20190717_1923"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="students",
            field=models.ManyToManyField(
                blank=True,
                related_name="courses_joined",
                to=settings.AUTH_USER_MODEL,
            ),
        )
    ]

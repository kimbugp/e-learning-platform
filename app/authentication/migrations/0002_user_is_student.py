# Generated by Django 2.2.3 on 2019-07-17 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_student',
            field=models.BooleanField(default=True),
        ),
    ]
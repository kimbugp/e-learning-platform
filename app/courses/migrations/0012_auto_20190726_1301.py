# Generated by Django 2.2.3 on 2019-07-26 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("courses", "0011_auto_20190726_0850")]

    operations = [
        migrations.AlterField(
            model_name="video", name="url", field=models.URLField(blank=True)
        )
    ]

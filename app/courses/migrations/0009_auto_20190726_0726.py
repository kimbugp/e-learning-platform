# Generated by Django 2.2.3 on 2019-07-26 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("courses", "0008_auto_20190726_0726")]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="image",
            field=models.FileField(upload_to="images"),
        )
    ]

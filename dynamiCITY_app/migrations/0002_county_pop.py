# Generated by Django 3.2.18 on 2023-04-11 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynamiCITY_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='county',
            name='pop',
            field=models.IntegerField(default=0),
        ),
    ]
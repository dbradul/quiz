# Generated by Django 3.1.6 on 2021-02-08 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_auto_20210208_1743'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='uuid',
        ),
    ]
# Generated by Django 3.1.6 on 2021-02-15 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_auto_20210211_1919'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='current_order_number',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]

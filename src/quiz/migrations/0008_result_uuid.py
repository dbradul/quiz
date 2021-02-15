# Generated by Django 3.1.6 on 2021-02-11 17:46

import core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_auto_20210208_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='uuid',
            field=models.UUIDField(db_index=True, default=core.utils.generate_uuid, unique=True),
        ),
    ]
# Generated by Django 3.1.6 on 2021-08-30 14:47

import core.utils
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='current_order_number',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='num_correct_answers',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(20)]),
        ),
        migrations.AddField(
            model_name='result',
            name='num_incorrect_answers',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(20)]),
        ),
        migrations.AddField(
            model_name='result',
            name='uuid',
            field=models.UUIDField(db_index=True, default=core.utils.generate_uuid, unique=True),
        ),
        migrations.AddField(
            model_name='result',
            name='write_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='test',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='test',
            name='uuid',
            field=models.UUIDField(db_index=True, default=core.utils.generate_uuid, unique=True),
        ),
        migrations.AddField(
            model_name='test',
            name='write_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='quiz.question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='order_number',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(20)]),
        ),
    ]

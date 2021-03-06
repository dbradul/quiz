# Generated by Django 3.1.6 on 2021-02-22 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('view_stats', 'View statistics')]},
        ),
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(default='default.jpg', null=True, upload_to='pics'),
        ),
        migrations.AddField(
            model_name='user',
            name='rating',
            field=models.PositiveSmallIntegerField(default=0, null=True),
        ),
    ]

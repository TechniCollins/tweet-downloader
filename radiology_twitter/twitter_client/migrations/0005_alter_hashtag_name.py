# Generated by Django 3.2.8 on 2021-10-22 06:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_client', '0004_alter_tweet_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hashtag',
            name='name',
            field=models.CharField(max_length=200, unique=True, validators=[django.core.validators.MinLengthValidator]),
        ),
    ]

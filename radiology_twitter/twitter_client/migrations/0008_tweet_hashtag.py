# Generated by Django 3.2.8 on 2021-10-22 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_client', '0007_alter_hashtag_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='hashtag',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]

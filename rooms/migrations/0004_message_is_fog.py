# Generated by Django 5.0 on 2023-12-24 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0003_alter_message_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_fog',
            field=models.BooleanField(default=False),
        ),
    ]
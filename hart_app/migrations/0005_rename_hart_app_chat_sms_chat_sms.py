# Generated by Django 5.1.3 on 2025-01-30 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hart_app', '0004_rename_chat_sms_hart_app_chat_sms'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='hart_app_chat_sms',
            new_name='chat_sms',
        ),
    ]

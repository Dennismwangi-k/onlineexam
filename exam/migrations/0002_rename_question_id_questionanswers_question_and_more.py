# Generated by Django 5.0.1 on 2024-01-18 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questionanswers',
            old_name='question_id',
            new_name='question',
        ),
        migrations.RemoveField(
            model_name='courses',
            name='user',
        ),
    ]

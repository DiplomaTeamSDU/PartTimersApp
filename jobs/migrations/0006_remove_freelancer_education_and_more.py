# Generated by Django 4.1.7 on 2023-03-27 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_freelancer_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='freelancer',
            name='education',
        ),
        migrations.RemoveField(
            model_name='freelancer',
            name='experience',
        ),
    ]

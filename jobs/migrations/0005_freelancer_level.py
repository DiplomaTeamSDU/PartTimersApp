# Generated by Django 4.1.7 on 2023-03-27 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_freelancer_education_specialization_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='freelancer',
            name='level',
            field=models.CharField(default='', max_length=15),
        ),
    ]
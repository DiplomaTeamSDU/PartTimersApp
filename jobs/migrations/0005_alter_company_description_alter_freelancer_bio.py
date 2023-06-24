# Generated by Django 4.1.7 on 2023-04-26 16:34

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_jobapplication_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='freelancer',
            name='bio',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]

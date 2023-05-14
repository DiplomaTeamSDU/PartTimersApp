# Generated by Django 4.1.7 on 2023-05-11 09:06

from django.db import migrations, models
import django.db.models.deletion
import jobs.validators


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0014_alter_freelancer_occupation_alter_job_position_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField(max_length=255)),
                ('file', models.FileField(blank=True, null=True, upload_to='freelancer_files/', validators=[jobs.validators.validate_is_pdf])),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('freelancer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.freelancer')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.job')),
            ],
        ),
    ]
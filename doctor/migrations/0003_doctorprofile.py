# Generated by Django 4.1.1 on 2022-10-29 05:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('doctor', '0002_rename_myuser_researcherprofile_researcher'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('M', 'MALE'), ('F', 'FEMALE')], default='M', max_length=1)),
                ('first_name', models.CharField(max_length=255)),
                ('license_key', models.CharField(max_length=255)),
                ('verified_admin', models.BooleanField(default=False)),
                ('last_name', models.CharField(max_length=255)),
                ('phone', models.IntegerField()),
                ('dob', models.DateField()),
                ('doctor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
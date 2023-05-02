# Generated by Django 3.2.18 on 2023-05-02 12:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('speciality', models.CharField(blank=True, max_length=100, null=True)),
                ('fee', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(blank=True, choices=[('Doctor', 'Doctor'), ('Patient', 'Patient'), ('Admin', 'Admin')], max_length=100, null=True)),
                ('cnic', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Slots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot_date', models.DateField(blank=True, null=True)),
                ('slot_start_time', models.TimeField(blank=True, null=True)),
                ('slot_end_time', models.TimeField(blank=True, null=True)),
                ('is_available', models.BooleanField(blank=True, default=True, null=True)),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hms.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disease_symptoms', models.CharField(blank=True, max_length=100, null=True)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient_profile', to='hms.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorsAvailibility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days', models.CharField(blank=True, max_length=100, null=True)),
                ('starting_time', models.TimeField(blank=True, null=True)),
                ('ending_time', models.TimeField(blank=True, null=True)),
                ('active', models.BooleanField(blank=True, default=True, null=True)),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hms.doctor')),
            ],
        ),
        migrations.AddField(
            model_name='doctor',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_profile', to='hms.userprofile'),
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hms.patient')),
                ('slots', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hms.slots')),
            ],
        ),
    ]

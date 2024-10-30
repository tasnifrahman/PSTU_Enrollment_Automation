# Generated by Django 5.1.2 on 2024-10-28 11:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('FacultyApp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=20, null=True, unique=True)),
                ('profile_pic', models.ImageField(upload_to='teachers_profile_pics/')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='FacultyApp.department')),
                ('faculty', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='FacultyApp.faculty')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Special_Course_Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseinfo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='FacultyApp.course')),
                ('teacher_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TeacherApp.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Course_Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseinfo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='FacultyApp.course')),
                ('teacher_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TeacherApp.teacher')),
            ],
        ),
        migrations.AddConstraint(
            model_name='teacher',
            constraint=models.UniqueConstraint(fields=('user', 'faculty', 'department'), name='unique_teacher'),
        ),
    ]
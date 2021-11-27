# Generated by Django 3.2.8 on 2021-11-09 18:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myproject', '0030_alter_tailieu_loaitl'),
    ]

    operations = [
        migrations.CreateModel(
            name='InformationUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Class', models.CharField(max_length=20)),
                ('Avatar', models.CharField(default='', max_length=100)),
                ('Gender', models.CharField(choices=[('Nam', 'Nam'), ('Nu', 'Nữ'), ('Khac', 'Khác')], default='Nam', max_length=10)),
                ('Facebook', models.CharField(default='', max_length=100)),
                ('Github', models.CharField(default='', max_length=100)),
                ('Bio', models.TextField()),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
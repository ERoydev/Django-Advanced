# Generated by Django 5.1.1 on 2024-10-08 19:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album_app', '0001_initial'),
        ('profile_app', '0002_alter_profile_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='albums', to='profile_app.profile'),
        ),
    ]

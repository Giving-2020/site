# Generated by Django 3.1.4 on 2020-12-02 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_ann_auth'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='ann_auth',
        ),
    ]

# Generated by Django 3.1.4 on 2020-12-02 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200603_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='ann_auth',
            field=models.BooleanField(default=False),
        ),
    ]
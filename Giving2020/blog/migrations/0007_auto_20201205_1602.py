# Generated by Django 3.1.4 on 2020-12-05 10:32

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20201203_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='content',
            field=markdownx.models.MarkdownxField(),
        ),
    ]

# Generated by Django 3.1.4 on 2020-12-05 10:33

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20201205_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='content',
            field=markdownx.models.MarkdownxField(),
        ),
    ]

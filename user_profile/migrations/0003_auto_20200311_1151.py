# Generated by Django 3.0.3 on 2020-03-11 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_auto_20200311_1145'),
    ]

    operations = [
        migrations.RenameField(
            model_name='savenews',
            old_name='news_categories',
            new_name='news',
        ),
    ]

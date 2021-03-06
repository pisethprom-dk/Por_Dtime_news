# Generated by Django 3.0.3 on 2020-03-12 04:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0011_auto_20200305_0734'),
        ('user_profile', '0003_auto_20200311_1151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='savenews',
            name='news',
        ),
        migrations.AddField(
            model_name='savenews',
            name='news',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='save_news', to='news.News'),
        ),
        migrations.AlterField(
            model_name='savenews',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_news', to=settings.AUTH_USER_MODEL),
        ),
    ]

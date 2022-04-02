# Generated by Django 3.2.7 on 2021-11-16 14:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_delete_cos_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='cos_like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.cos')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'cos_like',
            },
        ),
    ]
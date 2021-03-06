# Generated by Django 3.1.7 on 2021-09-17 05:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cos',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('brand', models.TextField(blank=True, null=True)),
                ('image', models.TextField(blank=True, null=True)),
                ('ingredient', models.TextField(blank=True, null=True)),
                ('prdname', models.TextField(blank=True, null=True)),
                ('price', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'cos',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ImageUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('pic', models.ImageField(upload_to='imageupload')),
            ],
        ),
        migrations.CreateModel(
            name='letter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('letters', models.CharField(max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='cos_like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.cos')),
            ],
            options={
                'db_table': 'cos_like',
            },
        ),
    ]

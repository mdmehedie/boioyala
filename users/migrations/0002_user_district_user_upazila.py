# Generated by Django 4.2.2 on 2023-07-18 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='district',
            field=models.CharField(default='cumilla', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='upazila',
            field=models.CharField(default='chandina', max_length=255),
            preserve_default=False,
        ),
    ]
# Generated by Django 5.0.2 on 2024-03-07 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='alt_image',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='src_image',
            field=models.URLField(null=True),
        ),
    ]

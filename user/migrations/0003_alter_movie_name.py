# Generated by Django 5.0.3 on 2024-04-02 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_movie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]

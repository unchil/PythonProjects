# Generated by Django 5.1 on 2024-10-02 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modeltest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fruit',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
    ]

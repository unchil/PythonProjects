# Generated by Django 5.1.2 on 2024-10-29 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplydemand', '0002_rename_basedatetime_currentsupplydemand_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentsupplydemand',
            name='index',
            field=models.TextField(primary_key=True, serialize=False),
        ),
    ]

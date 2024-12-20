# Generated by Django 5.1.2 on 2024-10-31 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplydemand', '0007_dayfiveminsupplydemand'),
    ]

    operations = [
        migrations.CreateModel(
            name='FullSupplyDemand',
            fields=[
                ('baseDatetime', models.TextField(primary_key=True, serialize=False)),
                ('suppAbility', models.FloatField(default=0.0)),
                ('currPwrTot', models.FloatField(default=0.0)),
                ('forecastLoad', models.FloatField(default=0.0)),
                ('suppReservePwr', models.FloatField(default=0.0)),
                ('suppReserveRate', models.FloatField(default=0.0)),
                ('operReservePwr', models.FloatField(default=0.0)),
                ('operReserveRate', models.FloatField(default=0.0)),
            ],
        ),
    ]

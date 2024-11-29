# Generated by Django 5.1.2 on 2024-10-31 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplydemand', '0006_rename_fiveminsupplydemand_fivemsupplydemand_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayFiveMinSupplyDemand',
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
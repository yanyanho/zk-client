# Generated by Django 3.0.8 on 2020-08-19 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zkclientapp', '0003_auto_20200810_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merkletree',
            name='mid',
            field=models.IntegerField(db_column='MID', primary_key=True, serialize=False),
        ),
    ]

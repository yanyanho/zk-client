# Generated by Django 3.0.8 on 2020-07-31 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zkserverapp', '0002_entry'),
    ]

    operations = [
        migrations.CreateModel(
            name='merkletree',
            fields=[
                ('mid', models.AutoField(db_column='MID', max_length=11, primary_key=True, serialize=False)),
                ('tree_data', models.TextField(db_column='tree_data', max_length=40000)),
            ],
            options={
                'db_table': 'merkletree',
            },
        ),
        migrations.DeleteModel(
            name='Entry',
        ),
        migrations.DeleteModel(
            name='Topic',
        ),
    ]

# Generated by Django 4.2.3 on 2023-08-26 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='price',
            new_name='buyprice',
        ),
        migrations.AddField(
            model_name='listing',
            name='startprice',
            field=models.FloatField(null=True),
        ),
    ]

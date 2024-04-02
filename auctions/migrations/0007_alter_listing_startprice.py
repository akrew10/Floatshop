# Generated by Django 4.2.3 on 2024-04-02 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_bid_user_alter_bid_bidprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='startprice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='startprice', to='auctions.bid'),
        ),
    ]
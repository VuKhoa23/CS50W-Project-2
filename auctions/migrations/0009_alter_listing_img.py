# Generated by Django 4.2.3 on 2023-07-25 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_bid_listing_placed_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='img',
            field=models.CharField(max_length=300),
        ),
    ]

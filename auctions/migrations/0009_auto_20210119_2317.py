# Generated by Django 3.1.5 on 2021-01-19 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20210119_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='listing',
            field=models.ManyToManyField(related_name='listings', to='auctions.Listing'),
        ),
    ]
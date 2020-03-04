# Generated by Django 3.0.4 on 2020-03-04 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(editable=False)),
                ('long_name', models.CharField(max_length=200)),
                ('short_name', models.CharField(blank=True, max_length=50, null=True)),
                ('market_price', models.IntegerField(blank=True, null=True)),
                ('trader_price', models.IntegerField(blank=True, null=True)),
                ('trader_name', models.CharField(blank=True, max_length=50, null=True)),
                ('trader_currency', models.CharField(blank=True, max_length=10, null=True)),
                ('slots', models.IntegerField(blank=True, null=True)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('width', models.IntegerField(blank=True, null=True)),
                ('rotated', models.BooleanField(default=0)),
                ('image', models.URLField(blank=True, max_length=400, null=True)),
                ('wiki_url', models.URLField(blank=True, max_length=400, null=True)),
                ('market_url', models.URLField(blank=True, max_length=400, null=True)),
            ],
        ),
    ]

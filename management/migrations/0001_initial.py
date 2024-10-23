# Generated by Django 4.2.16 on 2024-10-23 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Barangay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brgy_name', models.CharField(max_length=255)),
                ('brgy_voter_population', models.IntegerField(blank=True, null=True)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('long', models.FloatField(blank=True, null=True)),
            ],
            options={
                'ordering': ['brgy_name'],
            },
        ),
    ]

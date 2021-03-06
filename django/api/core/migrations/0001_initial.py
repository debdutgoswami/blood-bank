# Generated by Django 3.1.3 on 2020-11-27 06:41

import api.core.choices
import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line_1', models.CharField(max_length=40, verbose_name='Line 1')),
                ('address_line_2', models.CharField(blank=True, max_length=40, verbose_name='Line 2')),
                ('city', models.CharField(blank=True, max_length=40, verbose_name='City')),
                ('zipcode', models.CharField(max_length=6, verbose_name='Zipcode')),
                ('state', models.CharField(max_length=40, verbose_name='State')),
                ('country', models.CharField(choices=[], default=api.core.choices.Country['India'], max_length=2, verbose_name='Country')),
                ('coordinate', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='Co-ordinates')),
            ],
        ),
        migrations.CreateModel(
            name='RequestTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Name')),
                ('email', models.EmailField(blank=True, max_length=40, verbose_name='Email')),
                ('phone', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Phone Number')),
                ('bloodgroup', models.CharField(max_length=3, verbose_name='Blood Group')),
                ('created_on', models.DateField(auto_now=True, verbose_name='Created On')),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.address')),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Name')),
                ('email', models.EmailField(max_length=40, verbose_name='Email')),
                ('sex', models.CharField(blank=True, choices=[], max_length=1)),
                ('phone', models.CharField(blank=True, max_length=16, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Phone Number')),
                ('bloodgroup', models.CharField(choices=[], max_length=3, verbose_name='Blood Group')),
                ('age', models.PositiveSmallIntegerField(verbose_name='Age')),
                ('weight', models.PositiveSmallIntegerField(blank=True, verbose_name='Weight')),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.address')),
            ],
        ),
    ]

# Generated by Django 3.0.5 on 2021-07-14 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('user_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('user_password', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200, null=True)),
                ('address_detail', models.CharField(max_length=200, null=True)),
                ('recipient', models.CharField(max_length=200, null=True)),
                ('shipping_address', models.CharField(max_length=200, null=True)),
                ('phon_number_head', models.CharField(max_length=200, null=True)),
                ('phon_number_middle', models.CharField(max_length=200, null=True)),
                ('phon_number_tail', models.CharField(max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'user_info',
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_pk', models.CharField(max_length=100, null=True)),
                ('vendor_nm', models.CharField(max_length=100, null=True)),
                ('url', models.CharField(max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'vendor',
            },
        ),
        migrations.CreateModel(
            name='RequestVendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100)),
                ('vendor_pk', models.IntegerField()),
                ('vendor_id', models.CharField(max_length=200, null=True)),
                ('vendor_password', models.CharField(max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'request_vendor',
                'unique_together': {('user_id', 'vendor_pk')},
            },
        ),
    ]

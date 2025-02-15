# Generated by Django 4.1 on 2022-09-02 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('supplier_master', '0003_alter_supplier_master_mobile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temp_purchase_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(default=1)),
                ('stampdatetime', models.DateField(auto_now=True)),
                ('item_id', models.IntegerField()),
                ('rate', models.IntegerField()),
                ('quantity', models.IntegerField()),
            ],
            options={
                'db_table': 'temp_purchase_details',
            },
        ),
        migrations.CreateModel(
            name='Purchase_master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_no', models.IntegerField()),
                ('invoice_date', models.DateField()),
                ('status', models.IntegerField(default=1)),
                ('purchase_date', models.DateField(auto_now=True)),
                ('supplier_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier_master.supplier_master')),
            ],
            options={
                'db_table': 'purchase_master',
            },
        ),
        migrations.CreateModel(
            name='Purchase_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(default=1)),
                ('stampdatetime', models.DateField(auto_now=True)),
                ('item_id', models.IntegerField()),
                ('rate', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('fkey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase_master.purchase_master')),
            ],
            options={
                'db_table': 'purchase_details',
            },
        ),
    ]

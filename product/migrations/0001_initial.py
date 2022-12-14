# Generated by Django 3.2.9 on 2022-09-15 05:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=128, verbose_name='Nomi')),
                ('price', models.CharField(max_length=128, verbose_name='narxi')),
                ('amount', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=19)),
            ],
            options={
                'verbose_name': 'Mahsulot',
                'verbose_name_plural': 'Mahsulotlar',
            },
        ),
        migrations.CreateModel(
            name='ProductAmount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=19)),
                ('type', models.CharField(choices=[('plus', "Qo'shish"), ('minus', 'Ayirish')], max_length=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product', verbose_name='amount')),
            ],
            options={
                'verbose_name': 'Mahsulot soni',
                'verbose_name_plural': 'Mahsulot sonlari',
            },
        ),
    ]

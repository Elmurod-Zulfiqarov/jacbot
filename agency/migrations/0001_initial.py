# Generated by Django 3.2.9 on 2022-09-15 05:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('full_name', models.CharField(max_length=128, verbose_name="To'liq ismi: (F.I.SH)")),
                ('address', models.CharField(max_length=256, verbose_name="Manzili: (shahar/tuman, ko'cha, uy)")),
                ('phone', models.CharField(max_length=17, verbose_name='Telefon raqami: (+998 XX XXX XX XX)')),
                ('image', models.ImageField(upload_to='media/', verbose_name='Fotosurat')),
                ('image_passport', models.ImageField(upload_to='media/', verbose_name='Passportingiz fotosurati')),
            ],
            options={
                'verbose_name': 'Agent',
                'verbose_name_plural': 'Agentlar',
            },
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128, verbose_name='Firma nomi')),
                ('document', models.ImageField(upload_to='media/', verbose_name='Firma hujjati: (Guvohnoma, Patent)')),
                ('photo', models.ImageField(upload_to='media/', verbose_name="Do'kon fotosurati")),
                ('owner_full_name', models.CharField(max_length=128, verbose_name="To'liq ismi: (F.I.SH)")),
                ('phone', models.CharField(max_length=17, verbose_name='Telefon raqami: (+998 XX XXX XX XX)')),
                ('address', models.CharField(max_length=256, verbose_name="Manzili: (shahar/tuman, ko'cha, uy)")),
                ('location', models.JSONField(verbose_name="Location Jo'naitish")),
            ],
            options={
                'verbose_name': "Do'kon",
                'verbose_name_plural': "Do'konlar",
            },
        ),
        migrations.CreateModel(
            name='ProductGiven',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_given', to='agency.market', verbose_name="Do'kon")),
                ('product', models.ManyToManyField(related_name='product', to='product.Product')),
            ],
            options={
                'verbose_name': 'Berilgan mahsulot',
                'verbose_name_plural': 'Berilgan mahsulotlar',
            },
        ),
        migrations.CreateModel(
            name='PhotoReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('photo1', models.ImageField(upload_to='media', verbose_name='Foto hisobot')),
                ('photo2', models.ImageField(blank=True, null=True, upload_to='media', verbose_name='Foto hisobot')),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photo_report', to='agency.market', verbose_name="Do'kon")),
            ],
            options={
                'verbose_name': 'Foto hisobot',
                'verbose_name_plural': 'Foto hisobotlar',
            },
        ),
        migrations.CreateModel(
            name='MoneyReceivedDebt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cash', models.PositiveIntegerField(max_length=128, verbose_name='Naqd')),
                ('terminal', models.PositiveIntegerField(max_length=128, verbose_name='Terminal')),
                ('contract', models.PositiveIntegerField(max_length=128, verbose_name='Shartnoma')),
                ('get_all_money', models.CharField(max_length=128, verbose_name='Jami olingan pul')),
                ('debt', models.CharField(max_length=128, verbose_name="Do'konning qarzi")),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='money_received_debt', to='agency.market', verbose_name="Do'kon")),
            ],
            options={
                'verbose_name': 'Olingan pul va qarzdorlik',
                'verbose_name_plural': 'Olingan pullar va qarzdorliklar',
            },
        ),
    ]

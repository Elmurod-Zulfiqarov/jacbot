# Generated by Django 3.2.9 on 2022-09-15 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agency', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='is_view',
            field=models.BooleanField(default=False, verbose_name="Agent ma'lumotlarini tasdiqlash"),
        ),
        migrations.AlterField(
            model_name='agency',
            name='image_passport',
            field=models.ImageField(upload_to='media/', verbose_name='Passport fotosurati'),
        ),
    ]

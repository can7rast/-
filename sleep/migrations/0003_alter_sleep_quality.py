# Generated by Django 5.2.2 on 2025-06-05 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sleep', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sleep',
            name='quality',
            field=models.CharField(choices=[('отличный', 'Отличный'), ('хороший', 'Хороший'), ('средний', 'Средний'), ('плохой', 'Плохой'), ('очень плохой', 'Очень плохой')], max_length=50, verbose_name='Качество сна'),
        ),
    ]

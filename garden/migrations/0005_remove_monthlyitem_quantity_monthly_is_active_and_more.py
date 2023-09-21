# Generated by Django 4.2.5 on 2023-09-21 04:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0004_alter_monthly_month'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monthlyitem',
            name='quantity',
        ),
        migrations.AddField(
            model_name='monthly',
            name='is_active',
            field=models.BooleanField(default=True, help_text="Agar bu oylik hisobot tugatilsa bu atribut false bo'ladi"),
        ),
        migrations.AddField(
            model_name='monthlyitem',
            name='limit_quantity',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='monthlyitem',
            name='remaining_quantity',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='monthly',
            name='month',
            field=models.CharField(choices=[('Yanvar', 'Yanvar'), ('Fevral', 'Fevral'), ('Mart', 'Mart'), ('Aprel', 'Aprel'), ('May', 'May'), ('Iyun', 'Iyun'), ('Iyul', 'Iyul'), ('Avgust', 'Avgust'), ('Sentyabr', 'Sentyabr'), ('Oktyabr', 'Oktyabr'), ('Noyabr', 'Noyabr'), ('Dekabr', 'Dekabr')], max_length=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='garden.order'),
        ),
    ]

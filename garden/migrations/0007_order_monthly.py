# Generated by Django 4.2.5 on 2023-09-21 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0006_limit_limititem_delete_monthlyitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='monthly',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='garden.monthly'),
            preserve_default=False,
        ),
    ]

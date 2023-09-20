# Generated by Django 4.2.5 on 2023-09-20 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Monthly',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(choices=[(1, 'Yanvar'), (2, 'Fevral'), (3, 'Mart'), (4, 'Aprel'), (5, 'May'), (6, 'Iyun'), (7, 'Iyul'), (8, 'Avgust'), (9, 'Sentyabr'), (10, 'Oktyabr'), (11, 'Noyabr'), (12, 'Dekabr')], max_length=2)),
                ('year', models.CharField(max_length=4)),
                ('garden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garden.garden')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('garden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garden.garden')),
            ],
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.FloatField(verbose_name='Qoldiq')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garden.product')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garden.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garden.product')),
            ],
        ),
        migrations.CreateModel(
            name='MonthlyItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('price', models.IntegerField()),
                ('market_price', models.IntegerField()),
                ('monthly', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garden.monthly')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garden.product')),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('price', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('monthly', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garden.monthly')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garden.product')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Kun')),
                ('total_amount', models.IntegerField(default=0)),
                ('monthly', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garden.monthly', verbose_name='Oy')),
            ],
        ),
    ]

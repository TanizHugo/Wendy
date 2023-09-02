# Generated by Django 3.2.16 on 2023-03-26 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('merchant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_name', models.CharField(max_length=64, verbose_name='标签名')),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='merchant.merchant', verbose_name='商家ID')),
            ],
            options={
                'db_table': 'label',
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('sid', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='商品ID')),
                ('stock_name', models.CharField(max_length=64, unique=True, verbose_name='商品名')),
                ('price', models.FloatField(default=0.0, verbose_name='价格')),
                ('num', models.IntegerField(default=0, verbose_name='库存数量')),
                ('sold', models.IntegerField(default=0, verbose_name='已售数量')),
                ('type', models.IntegerField(verbose_name='类型')),
                ('flowers', models.CharField(max_length=64, verbose_name='主要花材')),
                ('material', models.CharField(max_length=64, verbose_name='使用材料')),
                ('package', models.CharField(max_length=64, verbose_name='鲜花包装')),
                ('lof', models.CharField(max_length=64, verbose_name='花语')),
            ],
            options={
                'db_table': 'stock',
            },
        ),
        migrations.CreateModel(
            name='StockLabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.label', verbose_name='标签ID')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.stock', verbose_name='商品ID')),
            ],
            options={
                'db_table': 'stock_label',
            },
        ),
        migrations.CreateModel(
            name='MerchantStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='merchant.merchant', verbose_name='商家ID')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.stock', verbose_name='商品ID')),
            ],
            options={
                'db_table': 'merchant_stock',
            },
        ),
    ]
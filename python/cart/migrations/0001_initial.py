# Generated by Django 3.2.16 on 2023-03-26 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stock', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopCart',
            fields=[
                ('openid', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='用户ID')),
                ('total_money', models.FloatField(default=0.0, verbose_name='购物车总价')),
                ('select_money', models.FloatField(default=0.0, verbose_name='选中物件价格')),
                ('num', models.IntegerField(default=0, verbose_name='购物车总数量')),
                ('select_all', models.BooleanField(default=False, verbose_name='是否全选')),
            ],
            options={
                'db_table': 'shop_cart',
            },
        ),
        migrations.CreateModel(
            name='CartStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='购买数量')),
                ('select_state', models.BooleanField(default=False, verbose_name='是否选中')),
                ('paid', models.BooleanField(default=False, verbose_name='是否支付')),
                ('shop_cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.shopcart', verbose_name='购物车ID')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.stock', verbose_name='商品ID')),
            ],
            options={
                'db_table': 'cart_stock',
            },
        ),
    ]
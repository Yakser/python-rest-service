# Generated by Django 4.0.5 on 2022-06-07 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_unit', '0003_alter_shopunit_parent_alter_shopunit_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopunit',
            name='type',
            field=models.CharField(choices=[('OFFER', 'OFFER'), ('CATEGORY', 'CATEGORY')], max_length=120, verbose_name='Тип элемента - категория или товар'),
        ),
    ]

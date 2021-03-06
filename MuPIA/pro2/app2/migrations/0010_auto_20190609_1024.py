# Generated by Django 2.1.7 on 2019-06-09 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0009_auto_20190608_1855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='benefits',
            name='employability',
            field=models.FloatField(default=0, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='benefits',
            name='externalities',
            field=models.FloatField(default=0, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='benefits',
            name='maintenance',
            field=models.FloatField(default=0, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='benefits',
            name='other_benefits',
            field=models.FloatField(default=0, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='benefits',
            name='value_growth',
            field=models.FloatField(default=0, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='benefits',
            name='work_efficiency',
            field=models.FloatField(default=0, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='costs',
            name='maintenance',
            field=models.FloatField(default=0, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='costs',
            name='management',
            field=models.FloatField(default=0, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='costs',
            name='other_costs',
            field=models.FloatField(default=0, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='costs',
            name='reduced_income',
            field=models.FloatField(default=0, max_length=150, null=True),
        ),
    ]

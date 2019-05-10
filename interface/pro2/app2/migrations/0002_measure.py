# Generated by Django 2.1.7 on 2019-05-10 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Measure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('cost', models.IntegerField()),
                ('lifetime', models.IntegerField()),
                ('electricity', models.IntegerField()),
                ('diesel_oil', models.IntegerField()),
                ('motor_gasoline', models.IntegerField()),
                ('natural_gas', models.IntegerField()),
                ('biomass', models.IntegerField()),
            ],
        ),
    ]

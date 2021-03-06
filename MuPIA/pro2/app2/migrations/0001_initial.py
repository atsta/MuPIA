# Generated by Django 2.1.7 on 2019-05-22 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Measure',
            fields=[
                ('name', models.CharField(max_length=150, primary_key=True, serialize=False, unique=True)),
                ('cost', models.FloatField(default=0)),
                ('lifetime', models.IntegerField(default=0)),
                ('description', models.TextField(default=None)),
                ('category', models.CharField(default=None, max_length=150)),
                ('measure_type', models.CharField(default=None, max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Social',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=150)),
                ('costs', models.CharField(default=None, max_length=150)),
                ('benefits', models.CharField(default=None, max_length=150)),
                ('discount_rate', models.FloatField(default=0.03)),
                ('analysis_period', models.IntegerField(default=25)),
                ('npv', models.FloatField(default=0)),
                ('b_to_c', models.FloatField(default=0)),
                ('irr', models.FloatField(default=0)),
                ('dpbp', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Benefits',
            fields=[
                ('measure', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app2.Measure')),
                ('energy_savings', models.FloatField(default=None, max_length=150)),
                ('maintenance', models.FloatField(default=None, max_length=150)),
                ('externalities', models.FloatField(default=None, max_length=150)),
                ('value_growth', models.FloatField(default=None, max_length=150)),
                ('work_efficiency', models.FloatField(default=None, max_length=150)),
                ('employability', models.FloatField(default=None, max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Costs',
            fields=[
                ('measure', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app2.Measure')),
                ('equipment', models.FloatField(default=None, max_length=150)),
                ('management', models.FloatField(default=None, max_length=150)),
                ('reduced_income', models.FloatField(default=None, max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Energy_Conservation',
            fields=[
                ('measure', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app2.Measure')),
                ('electricity3', models.FloatField(default=0)),
                ('diesel_oil3', models.FloatField(default=0)),
                ('motor_gasoline3', models.FloatField(default=0)),
                ('natural_gas3', models.FloatField(default=0)),
                ('biomass3', models.FloatField(default=0)),
                ('electricity7', models.FloatField(default=0)),
                ('diesel_oil7', models.FloatField(default=0)),
                ('motor_gasoline7', models.FloatField(default=0)),
                ('natural_gas7', models.FloatField(default=0)),
                ('biomass7', models.FloatField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='social',
            name='measure',
            field=models.ManyToManyField(to='app2.Measure'),
        ),
    ]

# Generated by Django 2.1.7 on 2019-06-08 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0008_auto_20190604_1534'),
    ]

    operations = [
        migrations.RenameField(
            model_name='costs',
            old_name='equipment',
            new_name='maintenance',
        ),
        migrations.RemoveField(
            model_name='benefits',
            name='energy_savings',
        ),
        migrations.AddField(
            model_name='benefits',
            name='other_benefits',
            field=models.FloatField(default=None, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='costs',
            name='other_costs',
            field=models.FloatField(default=None, max_length=150, null=True),
        ),
    ]

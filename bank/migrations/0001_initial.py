# Generated by Django 3.0.2 on 2020-01-29 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('negative_percent', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ('country', models.CharField(choices=[('ru', 'russia'), ('by', 'belarus'), ('ua', 'ukraine'), ('pl', 'poland')], max_length=2)),
            ],
            options={
                'verbose_name': 'Bank',
                'verbose_name_plural': 'Banks',
            },
        ),
    ]
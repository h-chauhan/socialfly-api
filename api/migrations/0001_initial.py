# Generated by Django 2.1.1 on 2018-09-30 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='InterestGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=4)),
                ('is_booked', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='interestgroup',
            name='end_seat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='end_seat', to='api.Seat'),
        ),
        migrations.AddField(
            model_name='interestgroup',
            name='interests',
            field=models.ManyToManyField(to='api.Interest'),
        ),
        migrations.AddField(
            model_name='interestgroup',
            name='start_seat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='start_seat', to='api.Seat'),
        ),
    ]

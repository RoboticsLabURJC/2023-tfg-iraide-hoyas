# Generated by Django 4.1.7 on 2023-12-30 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('edad', models.IntegerField()),
                ('pais', models.CharField(max_length=20)),
                ('sexo', models.CharField(max_length=20)),
                ('so', models.CharField(max_length=20)),
            ],
        ),
    ]

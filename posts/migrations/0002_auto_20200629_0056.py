# Generated by Django 2.2 on 2020-06-29 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-id']},
        ),
    ]

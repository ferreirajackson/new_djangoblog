# Generated by Django 2.2.13 on 2021-02-13 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0005_auto_20210211_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='categories',
            field=models.CharField(max_length=300, null=True),
        ),
    ]

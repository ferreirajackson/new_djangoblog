# Generated by Django 2.2.13 on 2021-03-14 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0014_post_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.CharField(max_length=255, null=True),
        ),
    ]

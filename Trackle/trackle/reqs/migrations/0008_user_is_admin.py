# Generated by Django 2.1.7 on 2019-03-19 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reqs', '0007_auto_20190319_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]

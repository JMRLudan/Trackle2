# Generated by Django 2.1.7 on 2019-03-19 02:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reqs', '0004_auto_20190319_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='Section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_section', to='reqs.Section'),
        ),
    ]

# Generated by Django 2.1.7 on 2019-10-11 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reqs', '0011_report_checked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requirement',
            name='duedate',
            field=models.DateField(verbose_name='Due Date'),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Requirement Name'),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='req_sub', to='reqs.Subject', verbose_name='Class'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Class Name'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='sypscience',
            field=models.BooleanField(verbose_name='SYP Science/Elective'),
        ),
    ]

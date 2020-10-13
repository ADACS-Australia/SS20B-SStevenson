# Generated by Django 2.2.14 on 2020-09-21 05:12

import compasweb.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compasweb', '0003_auto_20200909_2147'),
    ]

    operations = [
        migrations.CreateModel(
            name='COMPASModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('summary', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(max_length=1024)),
            ],
        ),
        migrations.RemoveField(
            model_name='compasjob',
            name='files',
        ),
        migrations.RemoveField(
            model_name='upload',
            name='compasjob',
        ),
        migrations.CreateModel(
            name='COMPASDatasetModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('files', models.FileField(blank=True, null=True, upload_to=compasweb.models.job_directory_path)),
                ('compasjob', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compasweb.COMPASJob')),
                ('compasmodel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compasweb.COMPASModel')),
            ],
        ),
        migrations.AddField(
            model_name='upload',
            name='datasetmodel',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='compasweb.COMPASDatasetModel'),
            preserve_default=False,
        ),
    ]
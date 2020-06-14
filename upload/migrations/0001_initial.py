# Generated by Django 3.0.7 on 2020-06-12 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file1', models.FileField(max_length=500, upload_to='excel_files/file1')),
                ('file2', models.FileField(max_length=500, upload_to='excel_files/file2')),
            ],
            options={
                'db_table': 'Excel Upload',
            },
        ),
    ]

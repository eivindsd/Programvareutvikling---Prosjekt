# Generated by Django 3.0.3 on 2020-02-29 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0026_auto_20200226_1310'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deltokarrangement',
            old_name='arrangementId',
            new_name='arrangement',
        ),
        migrations.RenameField(
            model_name='deltokarrangement',
            old_name='brukerId',
            new_name='bruker',
        ),
    ]
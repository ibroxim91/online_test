# Generated by Django 5.0.1 on 2024-01-29 10:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_history_is_marked_history_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='main.result'),
        ),
        migrations.AlterField(
            model_name='result',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='variant',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='main.question'),
        ),
    ]
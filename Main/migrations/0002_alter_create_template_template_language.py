# Generated by Django 5.1.5 on 2025-02-01 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='create_template',
            name='template_language',
            field=models.CharField(choices=[('en_US', 'English (US)'), ('es_ES', 'Spanish (Spain)'), ('fr_FR', 'French (France)'), ('de_DE', 'German (Germany)'), ('hi_IN', 'Hindi (India)')], default='en_US', max_length=100),
        ),
    ]

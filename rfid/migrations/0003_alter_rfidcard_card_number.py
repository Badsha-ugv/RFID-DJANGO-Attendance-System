# Generated by Django 5.0 on 2023-12-21 09:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rfid", "0002_userinfo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rfidcard",
            name="card_number",
            field=models.CharField(max_length=50),
        ),
    ]

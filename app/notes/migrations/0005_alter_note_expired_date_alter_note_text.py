# Generated by Django 5.0.2 on 2024-08-23 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notes", "0004_note_expired_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="note",
            name="expired_date",
            field=models.DateField(null=True, verbose_name="дата удаления"),
        ),
        migrations.AlterField(
            model_name="note",
            name="text",
            field=models.TextField(verbose_name="текст"),
        ),
    ]
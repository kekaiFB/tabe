# Generated by Django 4.1.7 on 2023-04-04 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("table_tgo", "0007_remove_ressourceoperation_office_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="tgo_object",
            options={
                "ordering": ["order"],
                "verbose_name": "Объект ТГО",
                "verbose_name_plural": "4 Объект ТГО",
            },
        ),
        migrations.AddField(
            model_name="tgo_object",
            name="order",
            field=models.PositiveIntegerField(default=1, verbose_name="Пункт"),
            preserve_default=False,
        ),
    ]

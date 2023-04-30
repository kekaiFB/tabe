# Generated by Django 4.1.7 on 2023-04-02 05:07

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ("table_tgo", "0003_alter_ressourceoperation_tgo_object"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ressourceoperation",
            name="ressource",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="res_operation",
                to="table_tgo.ressource",
                verbose_name="Ресурс",
            ),
        ),
        migrations.AlterField(
            model_name="ressourceoperation",
            name="tgo",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="res_operation",
                to="table_tgo.tgo",
                verbose_name="ТГО",
            ),
        ),
        migrations.AlterField(
            model_name="ressourceoperation",
            name="tgo_object",
            field=smart_selects.db_fields.ChainedForeignKey(
                chained_field="tgo",
                chained_model_field="tgo",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="res_operation",
                to="table_tgo.tgo_object",
                verbose_name="Объект ТГО",
            ),
        ),
    ]
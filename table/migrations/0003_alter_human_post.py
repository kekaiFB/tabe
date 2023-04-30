# Generated by Django 4.1.7 on 2023-04-18 07:05

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ("table", "0002_alter_human_post_alter_schedulenotjob_human_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="human",
            name="post",
            field=smart_selects.db_fields.ChainedForeignKey(
                chained_field="office",
                chained_model_field="office",
                on_delete=django.db.models.deletion.CASCADE,
                to="table.post",
                verbose_name="Должность",
            ),
        ),
    ]
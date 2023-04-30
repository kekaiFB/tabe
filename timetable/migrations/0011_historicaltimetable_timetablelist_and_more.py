# Generated by Django 4.1.7 on 2023-04-25 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("timetable", "0010_timetablelist"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicaltimetable",
            name="timetablelist",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="timetable.timetablelist",
                verbose_name="Плановое расписание",
            ),
        ),
        migrations.AddField(
            model_name="timetable",
            name="timetablelist",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="timetable.timetablelist",
                verbose_name="Плановое расписание",
            ),
            preserve_default=False,
        ),
    ]

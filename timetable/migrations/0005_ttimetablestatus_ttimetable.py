# Generated by Django 4.1.7 on 2023-04-19 14:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("timetable", "0004_flight_arrivalairport_flight_departurelairport"),
    ]

    operations = [
        migrations.CreateModel(
            name="TtimetableStatus",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=150, verbose_name="Название")),
            ],
            options={
                "verbose_name": "Статус расписания",
                "verbose_name_plural": "10 Статусы расписания",
            },
        ),
        migrations.CreateModel(
            name="Ttimetable",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("arrival_time", models.TimeField(verbose_name="Прилет")),
                ("departure_time", models.TimeField(verbose_name="Вылет")),
                (
                    "next_day_status",
                    models.BooleanField(default=False, verbose_name="Следующий день"),
                ),
                (
                    "start_register_time",
                    models.TimeField(verbose_name="Начало Регистрации"),
                ),
                (
                    "end_register_time",
                    models.TimeField(verbose_name="Конец Регистрации"),
                ),
                (
                    "date_start",
                    models.DateField(
                        blank=True, null=True, verbose_name="Начало действия"
                    ),
                ),
                (
                    "date_end",
                    models.DateField(
                        blank=True, null=True, verbose_name="Конец действия"
                    ),
                ),
                ("tgo", models.CharField(max_length=150, verbose_name="ТГО")),
                (
                    "comment",
                    models.CharField(
                        blank=True,
                        max_length=300,
                        null=True,
                        verbose_name="Комментарий",
                    ),
                ),
                (
                    "monday",
                    models.BooleanField(default=False, verbose_name="Понедельник"),
                ),
                ("tuesday", models.BooleanField(default=False, verbose_name="Вторник")),
                ("wednesday", models.BooleanField(default=False, verbose_name="Среда")),
                (
                    "thursday",
                    models.BooleanField(default=False, verbose_name="Четверг"),
                ),
                ("friday", models.BooleanField(default=False, verbose_name="Пятнциа")),
                (
                    "saturday",
                    models.BooleanField(default=False, verbose_name="Суббота"),
                ),
                (
                    "sunday",
                    models.BooleanField(default=False, verbose_name="Воскресенье"),
                ),
                (
                    "airline",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="timetable.airlines",
                        verbose_name="Аваиакомпания",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="author",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "editor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="editor",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "flight",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="timetable.flight",
                        verbose_name="Рейс",
                    ),
                ),
                (
                    "timetablestatusight",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="timetable.ttimetablestatus",
                        verbose_name="Статус",
                    ),
                ),
            ],
            options={
                "verbose_name": "Расписание",
                "verbose_name_plural": "11 Расписание",
            },
        ),
    ]
# -*- coding: utf-8 -*-
"""Таблицы базы данных и их запчасти.
"""
from collections import defaultdict
from dataclasses import asdict
from datetime import datetime, date, timedelta

import sqlalchemy
from sqlalchemy import exc

from pesky import cast, objects

engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)
metadata = sqlalchemy.MetaData(bind=engine)

Minutes = sqlalchemy.Table(
    'minutes',
    metadata,
    sqlalchemy.Column('minute', sqlalchemy.String(16), index=True),
    sqlalchemy.Column('category', sqlalchemy.String(255), index=True),
    sqlalchemy.UniqueConstraint('category', 'minute', name='uix_1')
)

Days = sqlalchemy.Table(
    'days',
    metadata,
    sqlalchemy.Column('day', sqlalchemy.String(16), index=True),
    sqlalchemy.Column('category', sqlalchemy.String(255), index=True),
    sqlalchemy.Column('minutes', sqlalchemy.Integer()),
    sqlalchemy.UniqueConstraint('category', 'day', name='uix_2'),
)

Weeks = sqlalchemy.Table(
    'weeks',
    metadata,
    sqlalchemy.Column('week', sqlalchemy.String(7), index=True),
    sqlalchemy.Column('category', sqlalchemy.String(255), index=True),
    sqlalchemy.Column('minutes', sqlalchemy.Integer()),
    sqlalchemy.UniqueConstraint('category', 'week', name='uix_3'),
)


def get_weeks(start: str, stop: str) -> list[tuple[str, str, int]]:
    """Извлечь данные из базы понедельно."""
    start_week = cast.to_week_num(start)
    stop_week = cast.to_week_num(stop)

    query = sqlalchemy.select(
        Weeks
    ).where(
        Weeks.c.week.between(start_week, stop_week)
    ).order_by(
        Weeks.c.week,
        Weeks.c.category,
    )

    with engine.begin() as conn:
        response = conn.execute(query)
        result = response.fetchall()

    return result


def get_minutes(start: str, stop: str) -> list[objects.Minute]:
    """Извлечь данные из базы поминутно."""
    query = sqlalchemy.select(
        Minutes
    ).where(
        Minutes.c.minute.between(start, stop)
    ).order_by(
        Minutes.c.minute,
        Minutes.c.category,
    )

    with engine.begin() as conn:
        response = conn.execute(query)
        result = [objects.Minute(*x) for x in response.fetchall()]

    return result


def get_days(start: str, stop: str) -> list[tuple]:
    """Извлечь данные из базы поминутно."""
    query = sqlalchemy.select(
        Days
    ).where(
        Days.c.day.between(start, stop)
    ).order_by(
        Days.c.day,
        Days.c.category,
    )

    with engine.begin() as conn:
        response = conn.execute(query)
        result = response.fetchall()

    return result


def dump_minutes(minutes: list[objects.Minute]) -> None:
    """Сохранить в базе поминутные данные."""
    stmt = sqlalchemy.insert(Minutes)

    with engine.begin() as conn:
        try:
            conn.execute(stmt, [asdict(x) for x in minutes])
        except exc.IntegrityError:
            pass


def recalc_days(start: datetime, stop: datetime) -> None:
    """Пересчитать в базе суточные данные."""
    start_left = f'{start.year:04d}-{start.month:02d}-{start.day:02d} 00:00'
    stop_right = f'{stop.year:04d}-{stop.month:02d}-{stop.day:02d} 23:59'
    minutes = get_minutes(start_left, stop_right)

    days = defaultdict(dict)

    for minute in minutes:
        date_ = minute.minute_dt.date()
        day = days[date_]

        if minute.category in day:
            day[minute.category] += 1
        else:
            day[minute.category] = 1

    dump_days(days)


def dump_days(days: dict[date, dict]) -> None:
    """Сохранить в базе поминутные данные."""

    with engine.begin() as conn:
        for date_, categories in days.items():
            for category, minutes in categories.items():
                stmt = sqlalchemy \
                    .insert(Days) \
                    .values(day=str(date_),
                            category=category,
                            minutes=minutes) \
                    .prefix_with('OR REPLACE')

                conn.execute(stmt)


def recalc_weeks(start: datetime, stop: datetime) -> None:
    """Пересчитать в базе посуточные данные."""
    start_week = start - timedelta(days=start.weekday())
    end_week = stop + timedelta(days=6)

    days = get_days(str(start_week.date()), str(end_week.date()))
    weeks = defaultdict(dict)

    for date_, category, minutes in days:
        week_num = cast.to_week_num(date_)
        week = weeks[week_num]

        if category in week:
            week[category] += minutes
        else:
            week[category] = minutes

    dump_weeks(weeks)


def dump_weeks(weeks: dict[str, dict[str, int]]) -> None:
    """Сохранить в базе понедельные данные."""

    with engine.begin() as conn:
        for week, categories in weeks.items():
            for category, minutes in categories.items():
                stmt = sqlalchemy \
                    .insert(Weeks) \
                    .values(week=week,
                            category=category,
                            minutes=minutes) \
                    .prefix_with('OR REPLACE')

                conn.execute(stmt)

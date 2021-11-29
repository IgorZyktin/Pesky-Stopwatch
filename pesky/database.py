# -*- coding: utf-8 -*-
"""Таблицы базы данных и их запчасти.
"""

import sqlalchemy

engine = sqlalchemy.create_engine('sqlite:///database.db', echo=False)
metadata = sqlalchemy.MetaData(bind=engine)

Minutes = sqlalchemy.Table(
    'minutes',
    metadata,
    sqlalchemy.Column('category', sqlalchemy.String(255), index=True),
    sqlalchemy.Column('minute', sqlalchemy.String(16), index=True),
    sqlalchemy.UniqueConstraint('category', 'minute', name='uix_1')
)

Days = sqlalchemy.Table(
    'days',
    metadata,
    sqlalchemy.Column('category', sqlalchemy.String(255), index=True),
    sqlalchemy.Column('day', sqlalchemy.String(16), index=True),
    sqlalchemy.Column('minutes', sqlalchemy.Integer()),
    sqlalchemy.UniqueConstraint('category', 'day', name='uix_2'),
)

Weeks = sqlalchemy.Table(
    'weeks',
    metadata,
    sqlalchemy.Column('category', sqlalchemy.String(255), index=True),
    sqlalchemy.Column('week', sqlalchemy.String(7), index=True),
    sqlalchemy.Column('minutes', sqlalchemy.Integer()),
    sqlalchemy.UniqueConstraint('category', 'week', name='uix_3'),
)


def get_weeks(start: str, stop: str) -> list:
    """Извлечь данные из базы понедельно."""
    # TODO
    return [
        ('01', 'Детальки', 120),
        ('02', 'Детальки', 50),
        ('03', 'Детальки', 70),
        ('04', 'Детальки', 94),
        ('05', 'Детальки', 22),
        ('06', 'Детальки', 50),
        ('07', 'Детальки', 73),
        ('08', 'Детальки', 11),
        ('09', 'Детальки', 75),
    ]


def dump_minutes(data: list) -> None:
    """Сохранить в базе поминутные данные."""
    # TODO


def dump_days(data: list) -> None:
    """Сохранить в базе суточные данные."""
    # TODO


def dump_weeks(data: list) -> None:
    """Сохранить в базе недельные данные."""
    # TODO

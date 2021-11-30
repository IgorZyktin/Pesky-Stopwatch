# -*- coding: utf-8 -*-
"""Бизнес логика.
"""
import io
from datetime import datetime, timedelta, date

import itertools

from pesky import cast
from pesky import objects
from pesky import parse

COLORS = [
    'red',
]

COLORS_GEN = itertools.cycle(COLORS)
COLORS_CACHE = {}


def get_start_and_stop(months: int) -> tuple[date, date]:
    """Сгенерировать начальную и конечную дату для анализа."""
    today = datetime.now().date()
    start = today - timedelta(days=months * 31)
    return start, today


def get_border_color(category: str) -> str:
    """Выбрать цвет для категории на графике."""
    color = COLORS_CACHE.get(category)

    if color is None:
        color = next(COLORS_GEN)
        COLORS_CACHE[category] = color

    return color


def analyze_payload(stream: io.BytesIO
                    ) -> tuple[datetime, datetime, list[objects.Minute]]:
    """Разложить сырые исходные данные в набор интервалов."""
    payload_bytes = cast.to_bytes(stream)
    payload = payload_bytes.decode('utf-8')
    spans = parse.ATimeLogger(payload).parse()

    min_m = '2100-01-01 00:00'
    max_m = '1970-01-01 00:00'

    minutes = []
    for span in spans:
        sub_minutes = cast.to_minutes(span)

        for sub_minute in sub_minutes:

            min_m = min(min_m, sub_minute.minute)
            max_m = max(max_m, sub_minute.minute)
            minutes.append(sub_minute)

    return cast.to_datetime(min_m), cast.to_datetime(max_m), minutes

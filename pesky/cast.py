# -*- coding: utf-8 -*-
"""Инструменты работы с данными.
"""
import io
import typing
from collections import defaultdict
from datetime import datetime, timedelta

from pesky import objects
from pesky.logic import get_border_color

PAYLOAD = list[tuple[str, str, int]]


def to_datetime(string: str) -> datetime:
    """Преобразовать строковую запись даты в экземпляр даты."""
    return datetime.strptime(string, '%Y-%m-%d %H:%M')


def to_week_num(string: str) -> str:
    """Преобразовать дату в номер недели."""
    date_ = datetime.strptime(string[0:10], '%Y-%m-%d').date()
    num = date_.isocalendar()[1]
    return f'{date_.year:04d}-{num:02d}'


def to_chartjs(payload: PAYLOAD) -> dict:
    """Конвертировать данные в формат ChartJS.

    На входе:
    [('01', 'Чесал кота', 120), ('02', 'Чесал кота', 50)]

    На выходе:
    {
        'labels': ['1', '2'],
        'datasets': [
            {
                'label': 'Чесал кота',
                'data': [120, 50],
                'borderColor': 'red'
            }
        ]
    }
    """
    raw_labels = set()
    raw_all_keys = set()
    by_type = defaultdict(dict)

    for key, category, duration in payload:
        key = key.strip()
        raw_all_keys.add(key)
        raw_labels.add(category)
        by_type[category][key] = duration

    labels = sorted(raw_labels)
    all_keys = sorted(raw_all_keys)

    datasets = []
    for category in labels:
        data = by_type[category]

        local_dataset = []
        for key in all_keys:
            local_dataset.append(data.get(key))

        datasets.append({
            'label': category,
            'data': local_dataset,
            'borderColor': get_border_color(category),
        })

    return {
        'labels': all_keys,
        'datasets': datasets,
    }


def to_bytes(stream: io.BytesIO) -> bytes:
    """Прочитать из потока все данные."""
    payload = bytearray()
    chunk_size = 4096

    while True:
        chunk = stream.read(chunk_size)

        if len(chunk) == 0:
            break

        payload += chunk

    return bytes(payload)


def to_minutes(span: objects.Span) -> typing.Iterator[objects.Minute]:
    """Нарезать отрезок времени на отдельные минуты."""
    if span.start_dt == span.stop_dt:
        yield objects.Minute(span.start, span.category)
        return

    current_minute = span.start_dt
    while current_minute <= span.stop_dt:
        yield objects.Minute(current_minute.strftime('%Y-%m-%d %H:%M'),
                             span.category)
        current_minute += timedelta(seconds=60)

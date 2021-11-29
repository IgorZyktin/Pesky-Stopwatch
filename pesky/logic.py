# -*- coding: utf-8 -*-
"""Бизнес логика.
"""

from collections import defaultdict
from datetime import datetime, timedelta, date

PAYLOAD = list[tuple[str, str, int]]


def get_start_and_stop(months: int) -> tuple[date, date]:
    """Сгенерировать начальную и конечную дату для анализа."""
    today = datetime.now().date()
    start = today - timedelta(days=months * 31)
    return start, today


def get_border_color(category: str) -> str:
    """Выбрать цвет для категории на графике."""
    # TODO
    return 'red'


def cast_to_chartjs(payload: PAYLOAD) -> dict:
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


def cast_payload(raw_payload: bytes) -> list:
    # TODO
    payload = raw_payload.decode('utf-8')
    print(payload)
    return []


def extract_start_and_stop(minutes: list) -> tuple[date, date]:
    # TODO
    return datetime.now().date(), datetime.now().date()

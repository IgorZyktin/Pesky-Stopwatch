# -*- coding: utf-8 -*-
"""Объекты для обмена данными.
"""

from dataclasses import dataclass
from datetime import datetime
from functools import cached_property


@dataclass
class Span:
    """Исходный отрезок времени."""
    category: str
    start: str
    stop: str

    @cached_property
    def start_dt(self) -> datetime:
        """Вернуть начало как время."""
        return datetime.strptime(self.start, '%Y-%m-%d %H:%M')

    @cached_property
    def stop_dt(self) -> datetime:
        """Вернуть конец как время."""
        return datetime.strptime(self.stop, '%Y-%m-%d %H:%M')


@dataclass
class Minute:
    """Отрезок времени в одну минуту."""
    minute: str
    category: str

    @cached_property
    def minute_dt(self) -> datetime:
        """Вернуть минуту как время."""
        return datetime.strptime(self.minute, '%Y-%m-%d %H:%M')

# -*- coding: utf-8 -*-
"""Парсеры для различных форматов.
"""
import traceback
import typing

from pesky import objects


class ATimeLogger:
    """Парсер для приложения aTimeLogger."""

    def __init__(self, text: str) -> None:
        """Инициализировать экземпляр."""
        self.text = text

    def parse(self) -> typing.Iterator[objects.Span]:
        """Разобрать исходные данные."""
        iterator = iter(self.text.strip().split('\n'))
        next(iterator)  # пропустить заголовок
        for line in iterator:
            if not line:
                break

            parts = [
                string
                for x in line.split(',')
                if (string := x.strip().strip('"'))
            ]
            category, _, start, stop = parts
            try:
                yield objects.Span(category, start, stop)
            except TypeError:
                print(parts)
                traceback.print_exc()
                raise

# -*- coding: utf-8 -*-
"""Запуск приложения.
"""
from pesky import app


def main():
    """Запуск приложения."""
    app.app.run('127.0.0.1', 7900, debug=True)


if __name__ == '__main__':
    main()
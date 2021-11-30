# -*- coding: utf-8 -*-
"""Запуск приложения.
"""
from pesky import app


def main():
    """Запуск приложения."""
    app.app.run('0.0.0.0', 5000, debug=True)


if __name__ == '__main__':
    main()

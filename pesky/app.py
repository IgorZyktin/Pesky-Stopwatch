# -*- coding: utf-8 -*-
"""Конструктор приложения.
"""

import flask

from pesky import cast
from pesky import database
from pesky import logic

app = flask.Flask(__name__)
database.metadata.create_all()


@app.route('/')
def index():
    """Стартовая страница."""
    return flask.render_template('index.html')


@app.route('/log/<int:months>')
def log(months: int):
    """Лог за X месяцев."""
    start, stop = logic.get_start_and_stop(months=months)
    return flask.redirect(flask.url_for('chart', start=start, stop=stop))


@app.route('/chart/<start>/<stop>')
def chart(start: str, stop: str):
    """График с данными."""
    return flask.render_template('chart.html', start=start, stop=stop)


@app.route('/api/chartjs/<start>/<stop>')
def api_chart(start: str, stop: str):
    """Ручка для получения данных по графикам."""
    weeks = database.get_weeks(start, stop)
    payload = cast.to_chartjs(weeks)
    return flask.jsonify(payload)


@app.route('/upload', methods=('GET', 'POST'))
def upload():
    """Загрузить данные."""
    if flask.request.method == 'POST':
        if 'file' in flask.request.files:
            file = flask.request.files['file']
            if file.filename and file.filename.lower().endswith('csv'):
                # noinspection PyTypeChecker
                min_m, max_m, minutes = logic.analyze_payload(file.stream)
                database.dump_minutes(minutes)
                database.recalc_days(min_m, max_m)
                database.recalc_weeks(min_m, max_m)
                return flask.redirect(flask.url_for('chart',
                                                    start=min_m, stop=max_m))

    return flask.render_template('upload.html')

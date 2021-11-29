# -*- coding: utf-8 -*-
"""Конструктор приложения.
"""

import flask

from pesky import database
from pesky import logic

app = flask.Flask(__name__)
database.metadata.create_all()


@app.route('/')
def index():
    """Стартовая страница."""
    context = {}
    return flask.render_template('index.html', **context)


@app.route('/one_month')
def one_month():
    """Лог за 1 месяц."""
    start, stop = logic.get_start_and_stop(months=1)
    return flask.redirect(flask.url_for('chart', start=start, stop=stop))


@app.route('/six_months')
def six_months():
    """Лог за 6 месяцев."""
    start, stop = logic.get_start_and_stop(months=6)
    return flask.redirect(flask.url_for('chart', start=start, stop=stop))


@app.route('/twelve_months')
def twelve_months():
    """Лог за 12 месяцев."""
    start, stop = logic.get_start_and_stop(months=12)
    return flask.redirect(flask.url_for('chart', start=start, stop=stop))


@app.route('/chart/<start>/<stop>')
def chart(start: str, stop: str):
    """График с данными."""
    return flask.render_template('chart.html', start=start, stop=stop)


@app.route('/api/chartjs/<start>/<stop>')
def api_chart(start: str, stop: str):
    """Ручка для получения данных по графикам."""
    weeks = database.get_weeks(start, stop)
    payload = logic.cast_to_chartjs(weeks)
    return flask.jsonify(payload)


@app.route('/upload', methods=('GET', 'POST'))
def upload():
    """Загрузить данные."""
    if flask.request.method == 'POST':
        if 'file' in flask.request.files:
            file = flask.request.files['file']
            if file.filename:
                payload = b''
                chunk_size = 4096
                while True:
                    chunk = file.stream.read(chunk_size)
                    if len(chunk) == 0:
                        break

                    payload += chunk

                clean_data = logic.cast_payload(payload)
                start, stop = logic.extract_start_and_stop(clean_data)
                database.dump_minutes(clean_data)
                return flask.redirect(flask.url_for('chart',
                                                    start=start, stop=stop))

    return flask.render_template('upload.html')

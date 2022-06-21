import logging
import hashlib
import hmac
import os.path
import subprocess
import threading
import traceback
from functools import partial
from pathlib import Path
from typing import Union

from flask import Flask, request, abort
from dotenv import dotenv_values

from deployer.config import parse_config

SOURCES_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SOURCES_DIR.parent


logging.basicConfig(
    format='%(levelname)s: %(asctime)s %(message)s', level=logging.DEBUG,
    filename=os.path.join(PROJECT_DIR, 'logs.log'), encoding='utf-8'
)

env_values = dotenv_values(os.path.join(PROJECT_DIR, '.env'))

app = Flask(__name__)

GITHUB_SECRET = env_values.get('GITHUB_SECRET')
REPO_NAME = 'Academy'
CONFIG_FILE_PATH = os.path.join(PROJECT_DIR, 'instances.toml')
CONFIG = parse_config(CONFIG_FILE_PATH)


@app.route('/ping')
def ping():
    return 'pong'


@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    """Эндпоинт для гитхаб вебхука."""
    # Достаем подпись из запроса
    signature = request.headers.get('X-Hub-Signature')
    if not signature or not signature.startswith('sha1='):
        logging.info('Отсутствует подпись')
        abort(400, 'X-Hub-Signature required')

    # Создаем локальный хэш данных запроса
    digest = hmac.new(
        GITHUB_SECRET.encode(), request.data, hashlib.sha1
    ).hexdigest()

    # Проверяем подпись
    if not hmac.compare_digest(signature, 'sha1=' + digest):
        logging.info('Неверная подпись')
        abort(400, 'Invalid signature')

    request_data = request.get_json()

    # Проверяем название репозитория на всякий случай
    if request_data.get('repository', {}).get('name') != REPO_NAME:
        logging.info('Неизвестный репозиторий')
        return "Don't care"

    instance, branch = get_update_path(request_data)
    if instance:
        logging.info('Нужно обновить')
        _update = partial(
            update, instance.get('project_path'), branch,
            instance.get('static_volume_name')
        )
        thread = threading.Thread(target=_update)
        thread.start()
    else:
        logging.info('Не нужно обновлять')

    logging.info('Success')
    return 'ok'


def get_update_path(request_data) -> tuple:
    pull_request_base = request_data.get('pull_request', {}).get('base', {}).get('ref')
    # Пытаемся из конфига достать данные обновляемого проекта по
    # названию ветки. Если достать не получилось, значит
    # обновлять проект не нужно.
    instance = CONFIG.get(pull_request_base)
    # Пулл реквест слили
    pull_request_merged = request_data.get('pull_request', {}).get('merged')
    # Если ПР слили в нужную ветку, возвращаем данные для обновления
    if pull_request_merged and instance:
        return instance, pull_request_base
    return None, pull_request_base


def update(path, branch, static_volume_name):
    """Вызывает bash скрипт пересборки контейнеров"""
    script_path = str(os.path.join(SOURCES_DIR, 'update.sh'))
    try:
        subprocess.call(f'.{script_path} {path} {branch} {static_volume_name}')
    except Exception:
        exc = traceback.format_exc()
        msg = 'Ошибка во время выполнения bash скрипта: \n' + exc
        logging.error(msg)


if __name__ == "__main__":
    app.run()

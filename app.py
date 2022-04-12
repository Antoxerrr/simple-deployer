import logging
import hashlib
import hmac
import subprocess
import threading
import traceback

from flask import Flask, request, abort
from dotenv import dotenv_values

logging.basicConfig(
    format='%(levelname)s: %(asctime)s %(message)s', level=logging.DEBUG,
    filename='logs.log', encoding='utf-8'
)

env_values = dotenv_values('.env')

app = Flask(__name__)

GITHUB_SECRET = env_values.get('GITHUB_SECRET')
REPO_NAME = 'Academy'


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

    if need_to_update(request_data):
        thread = threading.Thread(target=update)
        thread.start()

    logging.info('Success')
    return 'ok'


def need_to_update(request_data):
    """Разбирает payload от гитхаба и проверяет, нужно ли обновляться."""
    pull_request_base = request_data.get('pull_request', {}).get('base', {}).get('ref')
    # Ветка пулл реквеста = main
    pull_request_base_is_main = pull_request_base == 'main'
    # Пулл реквест слили
    pull_request_merged = request_data.get('pull_request', {}).get('merged')
    pull_request_merged_to_main = pull_request_base_is_main and pull_request_merged
    # Произошел пуш в main
    pushed_to_main = request_data.get('ref') == 'refs/heads/main'
    return pull_request_merged_to_main or pushed_to_main


def update():
    """Вызывает bash скрипт пересборки контейнеров"""
    try:
        subprocess.call('./update.sh')
    except Exception:
        exc = traceback.format_exc()
        msg = 'Ошибка во время выполнения bash скрипта: \n' + exc
        logging.error(msg)


if __name__ == "__main__":
    app.run()

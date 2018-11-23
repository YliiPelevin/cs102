
import requests
import time
import plotly
import plotly.graph_objs as go
import igraph
from igraph import Graph, plot
import numpy as np
from igraph import Graph, plot
from datetime import datetime
from collections import Counter
from config import VK_CONFIG, PLOTLY_CONFIG

config = {}
config.update(VK_CONFIG)
config.update(PLOTLY_CONFIG)
plotly.tools.set_credentials_file(
    username=config['PLOTLY_USERNAME'], api_key=config['PLOTLY_API_KEY'])


def get(url: str, params={}, timeout=5, max_retries=5, backoff_factor=0.3) -> requests.models.Response:
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    for retry in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=timeout)
            return response
        except requests.exceptions.RequestException:
            if retry == max_retries - 1:
                raise
            backoff_value = backoff_factor * (2 ** retry)
            time.sleep(backoff_value)


def get_friends(user_id: int, fields="")->dict:
    """ Вернуть данных о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    query_params = {
        'domain': "https://api.vk.com/method",
        'access_token': config['VK_ACCESS_TOKEN'],
        'user_id': user_id,
        'fields': fields,
        'v': '5.53'
    }

    url = "{}/friends.get".format(query_params['domain'])
    response = get(url, params=query_params)
    return response.json()


def messages_get_history(user_id: int, offset=0, count=20)->dict:
    """ Получить историю переписки с указанным пользователем

    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    max_count = 2000

    query_params = {
        'domain': "https://api.vk.com/method",
        'access_token': config['VK_ACCESS_TOKEN'],
        'user_id': user_id,
        'offset': offset,
        'count': min(count, max_count),
        'v': '5.53'
    }

    messages = []
    while max_count > 0:
        url = "{}/messages.getHistory".format("https://api.vk.com/method")
        response = requests.get(url, params=query_params)
        max_count -= 20
        query_params['offset'] += 20
        query_params['count'] = count
        messages.extend(response.json()['response']['items'])
        time.sleep(1)
    return messages

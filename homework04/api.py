import requests
import time
from config import VK_CONFIG, PLOTLY_CONFIG


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


def get_friends(user_id: int, fields="") -> dict:
    """ Вернуть данных о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    query_params = {
        'domain': "https://api.vk.com/method",
        'access_token': VK_CONFIG['VK_ACCESS_TOKEN'],
        'user_id': user_id,
        'fields': fields,
        'v': '5.53'
    }

    url = "{}/friends.get".format(query_params['domain'])
    response = get(url, params=query_params)
    return response.json()


def messages_get_history(user_id: int, offset=0, count=20) -> list:
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

    query_params = {
        'domain': "https://api.vk.com/method",
        'access_token': VK_CONFIG['VK_ACCESS_TOKEN'],
        'user_id': user_id,
        'offset': offset,
        'count': 200,
        'v': '5.53'
    }

    messages = []
    i = 0
    url = "{domain}/messages.getHistory?offset={offset}&count={count}&user_id={user_id}&" \
          "access_token={access_token}&v={version}"
    while i < count:
        if (i / 200) % 3 == 0 and i:
            time.sleep(1)
        if count - i <= 200:
            query_params['count'] = count - i
        url = url.format(**query_params)
        response = requests.get(url)
        json_doc = response.json()
        fail = json_doc.get('error')
        if fail:
            raise Exception(json_doc['error']['error_msg'])
        messages.extend(json_doc['response']['items'])
        i += 200
        query_params['offset'] += i
    return messages

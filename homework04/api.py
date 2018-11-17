
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

config = {
    'VK_ACCESS_TOKEN': 'e3e9333febd373f73776397585c25871061a9fa29c5171b6438734b714a6591b209bb28846af35c3f5f21',
    'PLOTLY_USERNAME': 'TolMalware',
    'PLOTLY_API_KEY': 'KUENWx0u8uPe5VfuxCm6'
}

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


def age_predict(user_id: int)->int:
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    friends = get_friends(user_id, 'bdate')
    all_dates = []
    for i in range(friends['response']['count']):
        if friends['response']['items'][i].get('bdate'):
            all_dates.append(friends['response']['items'][i]['bdate'])
    dates = [all_dates[i] for i in range(len(all_dates))
             if len(all_dates[i]) >= 8]
    ages = [2018 - int(i[-4:]) for i in dates]
    avg_age = int(sum(ages) / len(ages))
    return avg_age


def messages_get_history(user_id, offset=0, count=20):
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
    max_count =2000

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


def count_dates_from_messages(messages):
    """ Получить список дат и их частот

    :param messages: список сообщений
    """
    dates = [datetime.fromtimestamp(messages[i]['date']).strftime("%Y-%m-%d")
             for i in range(len(messages))]
    dates_stat = Counter(dates)
    x = [date for date in dates_stat]
    y = [dates_stat[date] for date in dates_stat]
    return x, y

def plotly_messages_freq(freq_list):
    """ Построение графика с помощью Plot.ly

    :param freq_list: список дат и их частот
    """
    data = [go.Scatter(x=freq_list[0], y=freq_list[1])]
    plotly.plotly.plot(data)



def get_network(user_id, as_edgelist=True):
    users_ids = get_friends(user_id)['response']['items']
    edges = []
    matrix = np.zeros((len(users_ids), len(users_ids)))
    for friend_1 in range(len(users_ids)):
        time.sleep(1)
        response = get_friends(users_ids[friend_1])
        if response.get('error'):
            continue
        friends = response['response']['items']
        for friend_2 in range(friend_1 + 1, len(users_ids)):
            if users_ids[friend_2] in friends:
                if as_edgelist:
                    edges.append((friend_1, friend_2))
                else:
                    matrix[friend_1][friend_2] = 1
    if as_edgelist:
        return edges
    else:
        return matrix


def plot_graph(user_id):
    surnames = get_friends(user_id, 'last_name')
    vertices = [surnames['response']['items'][i]['last_name']
                for i in range(len(surnames['response']['items']))]
    edges = get_network(user_id)
    g = Graph(vertex_attrs={"shape": "circle",
                            "label": vertices,
                            "size": 10},
              edges=edges, directed=False)

    N = len(vertices)
    visual_style = {
        "vertex_size": 20,
        "bbox": (2000, 2000),
        "margin": 100,
        "vertex_label_dist": 1.6,
        "edge_color": "gray",
        "autocurve": True,
        "layout": g.layout_fruchterman_reingold(
            maxiter=100000,
            area=N ** 2,
            repulserad=N ** 2)
    }

    clusters = g.community_multilevel()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)
    plot(g, **visual_style)

from collections import Counter
import datetime
import plotly
from typing import List, Tuple

from api import messages_get_history
from api_models import Message
from config import VK_CONFIG, PLOTLY_CONFIG

config = {}
config.update(VK_CONFIG)
config.update(PLOTLY_CONFIG)
Dates = List[datetime.date]
Frequencies = List[int]

plotly.tools.set_credentials_file(
    username=config['PLOTLY_USERNAME'], api_key=config['PLOTLY_API_KEY'])


def fromtimestamp(ts: int) -> datetime.date:
    return datetime.datetime.fromtimestamp(ts).date()


def count_dates_from_messages(messages: List[Message]) -> Tuple[Dates, Frequencies]:
    """ Получить список дат и их частот
    :param messages: список сообщений
    """
    dates = []
    freqs = []
    k = 0
    for m in messages:
        message = Message(**m)
        date = fromtimestamp(message.date)
        if date not in dates:
            if k:
                freqs.append(k)
            dates.append(date)
            k = 1
        else:
            k += 1
    freqs.append(k)
    freq_tuple = (dates, freqs)
    return freq_tuple


def plotly_messages_freq(dates: Dates, freq: Frequencies) -> None:
    """ Построение графика с помощью Plot.ly
    :param date: список дат
    :param freq: число сообщений в соответствующую дату
    """
    data = [plotly.graph_objs.Scatter(x=dates, y=freq)]
    plotly.plotly.plot(data)

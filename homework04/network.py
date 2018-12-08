from api import get_friends
import igraph
from igraph import Graph, plot
from typing import Union, List, Tuple
import np
import time


def get_network(user_id, as_edgelist=True):
    users_ids = get_friends(user_id)['response']['items']
    edges = []
    matrix = [[0] * len(users_ids) for _ in range(len(users_ids))]
    for friend_1 in range(len(users_ids)):
        time.sleep(0.33333334)
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


def plot_graph(user_id=505540783):
    surnames = get_friends(user_id, 'last_name')['response']['items']
    vertices = [surnames[i]['last_name'] for i in range(len(surnames))]
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

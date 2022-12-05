import random

gen_element = lambda x, owner=None: [x, None, None, owner]


def set_in_graph(z, graph):
    if z <= graph[0]:
        if graph[1] is None:
            graph[1] = gen_element(z, graph)
        else:
            set_in_graph(z, graph[1])
    else:
        if graph[2] is None:
            graph[2] = gen_element(z, graph)
        else:
            set_in_graph(z, graph[2])


def graph_sort(a, n):
    graph = gen_element(a[0])
    for i in range(1, n):
        set_in_graph(a[i], graph)
    return graph


def graph_to_line(graph):
    ar = []
    if graph[1] is not None:
        ar += graph_to_line(graph[1])
    ar.append(graph[0])
    if graph[2] is not None:
        ar += graph_to_line(graph[2])

    return ar


n = 20
a = [random.randint(0, 100) for i in range(n)]
print(a)

graph = graph_sort(a, n)

print(graph)
print(graph_to_line(graph))

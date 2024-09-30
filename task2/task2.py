import csv
from collections import defaultdict, deque

def load_from_csv(filename: str) -> str:
    graph = defaultdict(list)
    with open(filename, 'r') as file:
        for line in file.readlines():
            from_node, to_node = map(int, line.strip().split(','))
            graph[from_node].append(to_node)

    n = 5
    matrix = [[0] * n for _ in range(n)]
    for val in range(n):
        for keys in graph[val]:
            matrix[val - 1][keys - 1] = 1
            matrix[keys - 1][val - 1] = 1
    
    return matrix, graph

def calc_matrix(matrix: list, graph: dict) -> list:
    relation_matrix = [[0] * 5 for _ in range(len(matrix))]
    for i in range(len(matrix)):
        relation_matrix[i][0] = len(graph[i + 1]) if (i + 1) in graph else 0
        relation_matrix[i][1] = sum([1 if (i + 1) in nodes else 0 for nodes in graph.values()])
        relation_matrix[i][2] = 0 if relation_matrix[i][1] else relation_matrix[i][0]
        relation_matrix[i][3] = len([1 for p2, c2 in graph.items() for p1, c1 in graph.items() if (i+1) in c1 if p1 in c2])
        relation_matrix[i][4] = (lambda x: len(x) - 1 if (i + 1) in x else len(x))([c for p, c in graph.items() if i + 1 in c])

    return relation_matrix

def main(var: str) -> str:
    matrix, graph = load_from_csv(var)
    relation_matrix = calc_matrix(matrix, graph)
    with open('task3.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(relation_matrix)


if __name__ == '__main__':
    main('task2.csv')
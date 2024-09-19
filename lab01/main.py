import json

def read_from_json(filename):
    with open(filename, 'r') as stream:
        data = json.load(stream)
    
    nodes = data['nodes']
    n = len(nodes)

    matrix = [[0] * n for _ in range(n)]
    for val in range(1, n + 1):
        for keys in nodes[str(val)]:
            matrix[val - 1][int(keys) - 1] = 1
            matrix[int(keys) - 1][val - 1] = 1
    return matrix

def write_to_file(matrix, filename):
    n = len(matrix)
    graph = {'nodes': {}}

    for i in range(n):
        neigh = []
        for j in range(i + 1, n):
            if matrix[i][j]:
                neigh.append(str(j + 1))
        graph['nodes'][str(i + 1)] = neigh
    
    with open(filename, 'w') as file:
        json.dump(graph, file, indent=4)

if __name__ == '__main__':
    mat = read_from_json('graph.json')
    write_to_file(mat, 'mem.json')
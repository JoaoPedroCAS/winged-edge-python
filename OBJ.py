import random  # Importa o módulo random para possíveis usos futuros

# Definindo a classe Vertex (vértice)
class Vertex:
    def __init__(self, vertex_id):
        self.vertex_id = vertex_id  # Atribui um ID único a cada vértice
        self.edges = []  # Lista de arestas conectadas a este vértice
        self.faces = []  # Lista de faces conectadas a este vértice

# Definindo a classe Edge (aresta)
class Edge:
    def __init__(self, vertex1, vertex2):
        self.vertex1 = vertex1  # Primeiro vértice da aresta
        self.vertex2 = vertex2  # Segundo vértice da aresta
        self.faces = []  # Lista de faces conectadas a esta aresta

# Definindo a classe Face (face)
class Face:
    def __init__(self, vertices):
        self.vertices = vertices  # Lista de vértices que compõem a face
        self.edges = []  # Lista de arestas que compõem a face

# Função para construir a estrutura de dados Winged Edge
def build_winged_edge_structure(file_path):
    vertices = []  # Lista de vértices
    edges = []  # Lista de arestas
    faces = []  # Lista de faces

    # Abre o arquivo OBJ especificado para leitura
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                # Processa as linhas que começam com 'v ' como vértices
                values = line.split()[1:]  # Separa os valores da linha
                vertex = Vertex(len(vertices) + 1)  # Cria um novo vértice com ID único
                vertices.append(vertex)  # Adiciona o vértice à lista de vértices
            elif line.startswith('f '):
                # Processa as linhas que começam com 'f ' como faces
                values = line.split()[1:]  # Separa os valores da linha
                vertex_ids = [int(v.split('/')[0]) for v in values]  # Extrai IDs dos vértices
                face = Face([vertices[id - 1] for id in vertex_ids])  # Cria uma nova face com vértices
                faces.append(face)  # Adiciona a face à lista de faces

    # Conecta vértices, arestas e faces
    for face in faces:
        for i, vertex in enumerate(face.vertices):
            vertex.faces.append(face)  # Adiciona a face à lista de faces do vértice

            v1 = vertex
            v2 = face.vertices[(i + 1) % len(face.vertices)]  # Obtém o próximo vértice na lista
            edge = None

            # Verifica se a aresta já existe ou cria uma nova
            for e in edges:
                if (e.vertex1 == v1 and e.vertex2 == v2) or (e.vertex1 == v2 and e.vertex2 == v1):
                    edge = e
                    break

            if edge is None:
                edge = Edge(v1, v2)  # Cria uma nova aresta
                edges.append(edge)  # Adiciona a aresta à lista de arestas

            edge.faces.append(face)  # Adiciona a face à lista de faces da aresta
            face.edges.append(edge)  # Adiciona a aresta à lista de arestas da face
            vertex.edges.append(edge)  # Adiciona a aresta à lista de arestas do vértice

    return vertices, edges, faces  # Retorna as listas de vértices, arestas e faces

# Loop para carregar objetos e consultar informações
while True:
    chosen_object = input("Enter the name of the object you want to load (cube, square, circle, etc.): ")
    object_file = f'{chosen_object}.obj'  # Constrói o nome do arquivo OBJ com base na entrada do usuário
    try:
        vertices, edges, faces = build_winged_edge_structure(object_file)  # Tenta construir a estrutura
        break  # Sai do loop se o arquivo for encontrado
    except FileNotFoundError:
        print("Object not found. Please try again.")  # Manipula a exceção se o arquivo não for encontrado

selected_vertex_id = int(input("Enter the vertex ID you want to access faces: "))  # Solicita o ID do vértice
selected_edge_id = int(input("Enter the edge ID you want to access edges: "))  # Solicita o ID da aresta
selected_face_id = int(input("Enter the face ID you want to access vertices: "))  # Solicita o ID da face

vertex_id = selected_vertex_id  # Atribui o ID do vértice selecionado
if vertex_id < 1 or vertex_id > len(vertices):
    print("Error: Vertex does not exist!")  # Verifica se o ID do vértice é válido e exibe uma mensagem de erro, se necessário
else:
    vertex = vertices[vertex_id - 1]  # Obtém o vértice correspondente com base no ID
    shared_faces = [face for face in vertex.faces]  # Lista de faces compartilhadas pelo vértice
    print(f"Faces shared by vertex {vertex_id}:")
    for face in shared_faces:
        vertex_ids_face = ', '.join(str(v.vertex_id) for v in face.vertices)
        print(f"Face: {vertex_ids_face}")  # Exibe as faces compartilhadas pelo vértice

edge_id = selected_edge_id  # Atribui o ID da aresta selecionada
if edge_id < 1 or edge_id > len(vertices):
    print("Error: Edge does not exist!")  # Verifica se o ID da aresta é válido e exibe uma mensagem de erro, se necessário
else:
    edge = edges[edge_id - 1]  # Obtém a aresta correspondente com base no ID
    shared_edges = [edge for edge in vertex.edges]  # Lista de arestas compartilhadas pelo vértice
    print(f"Edges shared by vertex {edge_id}:")
    for shared_edge in shared_edges:
        print(shared_edge.vertex1.vertex_id, shared_edge.vertex2.vertex_id)  # Exibe as arestas compartilhadas pelo vértice

face_id = selected_face_id  # Atribui o ID da face selecionada
if face_id < 1 or face_id > len(faces):
    print("Error: Face does not exist!")  # Verifica se o ID da face é válido e exibe uma mensagem de erro, se necessário
else:
    face = faces[face_id - 1]  # Obtém a face correspondente com base no ID
    shared_vertices = [vertex for vertex in face.vertices]  # Lista de vértices

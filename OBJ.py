import random

# Definindo a classe Vertex (vértice)
class Vertex:
    def __init__(self, vertex_id):
        self.vertex_id = vertex_id  # Inicializa o ID do vértice
        self.edges = []  # Inicializa uma lista vazia para armazenar as arestas conectadas a este vértice
        self.faces = []  # Inicializa uma lista vazia para armazenar as faces conectadas a este vértice

# Definindo a classe Edge (aresta)
class Edge:
    def __init__(self, vertex1, vertex2):
        self.vertex1 = vertex1  # Inicializa o primeiro vértice da aresta
        self.vertex2 = vertex2  # Inicializa o segundo vértice da aresta
        self.faces = []  # Inicializa uma lista vazia para armazenar as faces conectadas a esta aresta

# Definindo a classe Face (face)
class Face:
    def __init__(self, vertices):
        self.vertices = vertices  # Inicializa a lista de vértices que compõem a face
        self.edges = []  # Inicializa uma lista vazia para armazenar as arestas que compõem a face

# Função para construir a estrutura de dados Winged Edge
def build_winged_edge_structure(file_path):
    vertices = []  # Inicializa uma lista vazia para armazenar os vértices do modelo
    edges = []  # Inicializa uma lista vazia para armazenar as arestas do modelo
    faces = []  # Inicializa uma lista vazia para armazenar as faces do modelo

    # Abre o arquivo OBJ especificado para leitura
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                # Processa as linhas que começam com 'v ' como vértices
                values = line.split()[1:]  # Divide a linha em valores
                vertex = Vertex(len(vertices) + 1)  # Cria um novo vértice com um ID único
                vertices.append(vertex)  # Adiciona o vértice à lista de vértices
            elif line.startswith('f '):
                # Processa as linhas que começam com 'f ' como faces
                values = line.split()[1:]  # Divide a linha em valores
                vertex_ids = [int(v.split('/')[0]) for v in values]  # Extrai os IDs dos vértices
                face = Face([vertices[id - 1] for id in vertex_ids])  # Cria uma nova face com base nos vértices
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

# Função para listar informações sobre vértices
def list_vertex_info(vertices):
    selected_vertex_id = int(input("Enter the vertex ID you want to access faces: "))  # Solicita o ID do vértice

    # Verificação de ID válido para vértices
    if selected_vertex_id < 1 or selected_vertex_id > len(vertices):
        print("Error: Vertex does not exist!")
    else:
        vertex = vertices[selected_vertex_id - 1]  # Obtém o vértice correspondente com base no ID
        shared_faces = vertex.faces  # Lista de faces compartilhadas pelo vértice

        if not shared_faces:
            print(f"No faces shared by vertex {selected_vertex_id}")
        else:
            print(f"Faces shared by vertex {selected_vertex_id}:")
            for face in shared_faces:
                vertex_ids_face = ', '.join(str(v.vertex_id) for v in face.vertices)
                print(f"Face vertices: [{vertex_ids_face}]")

# Função para listar informações sobre arestas
def list_edge_info(edges):
    selected_edge_id = int(input("Enter the edge ID you want to access edges: "))  # Solicita o ID da aresta

    # Verificação de ID válido para arestas
    if selected_edge_id < 1 or selected_edge_id > len(edges):
        print("Error: Edge does not exist!")
    else:
        edge = edges[selected_edge_id - 1]  # Obtém a aresta correspondente com base no ID
        shared_faces = edge.faces  # Lista de faces compartilhadas pela aresta

        if not shared_faces:
            print(f"No faces shared by edge {selected_edge_id}")
        else:
            print(f"Faces shared by edge {selected_edge_id}:")
            for face in shared_faces:
                vertex1_id = face.vertices[0].vertex_id
                vertex2_id = face.vertices[1].vertex_id
                print(f"Edge vertices: {vertex1_id}, {vertex2_id}")

# Função para listar informações sobre faces
def list_face_info(faces):
    selected_face_id = int(input("Enter the face ID you want to access vertices: "))  # Solicita o ID da face

    # Verificação de ID válido para faces
    if selected_face_id < 1 or selected_face_id > len(faces):
        print("Error: Face does not exist!")
    else:
        face = faces[selected_face_id - 1]  # Obtém a face correspondente com base no ID
        shared_vertices = face.vertices  # Lista de vértices

        if not shared_vertices:
            print(f"No vertices in face {selected_face_id}")
        else:
            print(f"Vertices in face {selected_face_id}:")
            for shared_vertex in shared_vertices:
                print(f"Vertex ID: {shared_vertex.vertex_id}")

# Loop principal para carregar objetos e consultar informações
while True:
    chosen_object = input("Enter the name of the object you want to load (cube, square, circle, etc.): ")
    object_file = f'{chosen_object}.obj'

    try:
        vertices, edges, faces = build_winged_edge_structure(object_file)
        break
    except FileNotFoundError:
        print("Object not found. Please try again.")

# Menu interativo para listar informações
while True:
    print("\nMenu:")
    print("1. List information about vertices")
    print("2. List information about edges")
    print("3. List information about faces")
    print("4. Exit")
    
    choice = input("Enter your choice (1/2/3/4): ")

    if choice == "1":
        list_vertex_info(vertices)
    elif choice == "2":
        list_edge_info(edges)
    elif choice == "3":
        list_face_info(faces)
    elif choice == "4":
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please enter a valid option.")

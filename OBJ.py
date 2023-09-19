import PySimpleGUI as sg
import os

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
        self.face_ids = []  # Inicializa uma lista vazia para armazenar os IDs das faces conectadas a esta aresta

    def add_face(self, face_id):
        self.face_ids.append(face_id)

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
    for face_id, face in enumerate(faces, start=1):
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

            edge.add_face(face_id)  # Adiciona o ID da face à lista de IDs de faces da aresta
            face.edges.append(edge)  # Adiciona a aresta à lista de arestas da face
            vertex.edges.append(edge)  # Adiciona a aresta à lista de arestas do vértice

    return vertices, edges, faces  # Retorna as listas de vértices, arestas e faces

# Função para listar informações sobre vértices
def list_vertex_info(vertex, edges):
    if not vertex:
        sg.popup("Error: Vertex does not exist!")
        return

    shared_edges = vertex.edges  # Lista de arestas compartilhadas pelo vértice

    if not shared_edges:
        sg.popup(f"No edges shared by vertex {vertex.vertex_id}")
    else:
        edge_ids = [edges.index(edge) + 1 for edge in shared_edges]
        sg.popup(f"Edges shared by vertex {vertex.vertex_id}:", ', '.join(map(str, edge_ids)))

# Função para listar informações sobre arestas
def list_edge_info(edges, selected_edge_id):
    Flist = ""

    # Verificação de ID válido para arestas
    if selected_edge_id < 1 or selected_edge_id > len(edges):
        sg.popup("Error: Edge does not exist!")
    else:
        edge = edges[selected_edge_id - 1]  # Obtém a aresta correspondente com base no ID
        shared_faces = edge.face_ids  # Lista de IDs de faces compartilhadas pela aresta

        if not shared_faces:
            sg.popup(f"No faces shared by edge {selected_edge_id}")
        else:
            sg.popup(f"Faces shared by edge {selected_edge_id}:", ', '.join(map(str, shared_faces)))

# Função para listar informações sobre faces
def list_face_info(faces, selected_face_id):
    Vlist = ""
    # Verificação de ID válido para faces
    if selected_face_id < 1 or selected_face_id > len(faces):
        sg.popup("Error: Face does not exist!")
    else:
        face = faces[selected_face_id - 1]  # Obtém a face correspondente com base no ID
        shared_vertices = face.vertices  # Lista de vértices

        if not shared_vertices:
            sg.popup(f"No vertices in face {selected_face_id}")
        else:
            for shared_vertex in shared_vertices:
                Vlist = Vlist + (f"Vertex ID: {shared_vertex.vertex_id}" + "\n")
            sg.popup(f"Vertices in face {selected_face_id}:", Vlist)

sg.theme('DarkAmber')  # Adicione um toque de cor

# Todas as coisas dentro da sua janela.
layout = [[sg.Text('Winged Edge Structure')],
          [sg.Text('Enter the name of the object you want to load (cube, square, circle, etc.):'),
           sg.InputText()],
          [sg.Button('Ok'), sg.Button('Cancel')]]

# Crie a Janela
window = sg.Window('Window Title', layout)

# Loop de Eventos para processar "eventos" e obter os "valores" das entradas
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':  # Se o usuário fechar a janela ou clicar em Cancel
        break

    chosen_object = values[0]
    path = os.path.dirname(os.path.abspath(__file__))  # Obtém a pasta atual
    path = path + "\\" + chosen_object + ".obj"

    object_file = path

    try:
        vertices, edges, faces = build_winged_edge_structure(object_file)
        sg.popup('Object loaded successfully!')
        break
    except FileNotFoundError:
        print("Object not found. Please try again.")
        sg.popup('Object not found. Please try again.')

window.close()

layout = [[sg.Text('Some text on Row 1')],
          [sg.Text('Enter the vertex ID you want to access edges:'), sg.InputText()],
          [sg.Text('Enter the edge ID you want to access faces:'), sg.InputText()],
          [sg.Text('Enter the face ID you want to access vertices:'), sg.InputText()],
          [sg.OK(), sg.Cancel()]]

# Crie a Janela
window = sg.Window('Window Title', layout)

# Loop de Eventos para processar "eventos"
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break

    if values[0] != "":  # Primeiro campo solicitado
        operation = int(values[0])
        selected_vertex = vertices[operation - 1] if 1 <= operation <= len(vertices) else None
        list_vertex_info(selected_vertex, edges)

    if values[1] != "":  # Segundo campo solicitado
        operation = int(values[1])
        list_edge_info(edges, operation)

    if values[2] != "":  # Terceiro campo solicitado
        operation = int(values[2])
        list_face_info(faces, operation)

window.close()

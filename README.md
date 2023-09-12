# Documentação para o Código

## Introdução
Este documento fornece uma visão geral do código Python que lida com a leitura de arquivos no formato OBJ e constrói uma estrutura de dados Winged Edge para representar objetos 3D. O código permite que os usuários carreguem objetos 3D a partir de arquivos OBJ e consultem informações sobre vértices, arestas e faces desses objetos.

## Estrutura do Código
O código é organizado em três classes principais: `Vertex`, `Edge` e `Face`, que representam vértices, arestas e faces, respectivamente. Além disso, há uma função principal chamada `build_winged_edge_structure` que realiza a leitura do arquivo OBJ e a construção da estrutura Winged Edge.

### Classes Principais
- `Vertex`: Representa um vértice 3D com um ID único, uma lista de arestas conectadas a ele e uma lista de faces conectadas a ele.
- `Edge`: Representa uma aresta entre dois vértices com referências a esses vértices e uma lista de faces conectadas a ela.
- `Face`: Representa uma face definida por uma lista de vértices e uma lista de arestas que a compõem.

### Função Principal
- `build_winged_edge_structure(file_path)`: Esta função é responsável por ler o arquivo OBJ especificado e construir a estrutura de dados Winged Edge com base nas definições de vértices, arestas e faces presentes no arquivo. Ela retorna três listas: uma lista de vértices, uma lista de arestas e uma lista de faces.

### Uso do Código
O código inclui um loop que permite ao usuário carregar objetos 3D a partir de arquivos OBJ e consultar informações sobre eles. O usuário pode inserir o nome do objeto desejado, e o código tentará carregar o arquivo correspondente. Após o carregamento bem-sucedido, o usuário pode inserir IDs de vértices, arestas e faces para consultar informações sobre eles.

## Requisitos
Para executar este código, você precisará do seguinte:
- Python 3.x instalado em seu sistema.

## Execução do Código
1. Execute o código Python.
2. Insira o nome do objeto que deseja carregar quando solicitado.
3. O código tentará carregar o arquivo OBJ correspondente.
4. Após o carregamento bem-sucedido, insira IDs de vértices, arestas e faces para consultar informações sobre o objeto.

# Documentação para o Formato do Arquivo OBJ

## Introdução
Este documento descreve o formato do arquivo OBJ usado para representar objetos 3D. O formato OBJ é amplamente utilizado na indústria de gráficos 3D e é uma maneira comum de descrever geometria de malhas 3D.

## Estrutura do Arquivo
Um arquivo OBJ é dividido em várias seções, incluindo:

- Comentários: Linhas começando com `#` são consideradas comentários e são ignoradas.
- Vértices: Linhas começando com `v` definem vértices 3D com coordenadas x, y e z.
- Normais de Vértice: Linhas começando com `vn` definem normais de vértice que são usadas para cálculos de iluminação.
- Faces: Linhas começando com `f` definem faces, especificando os índices de vértices que compõem a face.

### Exemplo de Formato OBJ
```
# cube.obj
#
g cube
v  0.0  0.0  0.0
v  0.0  0.0  5.0
v  0.0  5.0  0.0
...
vn  0.0  0.0  1.0
vn  0.0  0.0 -1.0
...
f  1//2  7//2  5//2
f  1//2  3//2  7//2
...
```

### Linhas `f` (Faces)
As linhas `f` definem faces, onde os índices se referem aos vértices definidos anteriormente. O formato comum é `f v1//vn1 v2//vn2 v3//vn3 ...`, onde `v1`, `v2`, `v3` são índices de vértices e `vn1`, `vn2`, `vn3` são índices de

 normais de vértice. No exemplo acima, as normais são omitidas usando `//`.

## Considerações Finais
Este formato OBJ é amplamente suportado por ferramentas de modelagem 3D e é uma escolha popular para importar e exportar geometria 3D devido à sua simplicidade e flexibilidade.

Lembre-se de que esta documentação fornece uma visão geral dos principais elementos do arquivo OBJ, e é recomendável consultar a documentação oficial do formato OBJ para obter informações mais detalhadas.

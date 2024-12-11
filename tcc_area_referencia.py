import numpy as np
from PIL import Image
import networkx as nx
import community
import matplotlib.pyplot as plt

img = Image.open('declive_merg_repr.tif')

img_array = np.array(img)
height, width = img_array.shape

new_matrix = np.empty([height, width])
community_image = np.zeros((height, width, 3), dtype=np.uint8)

print(height, width)

for i in range(height):
    for j in range(width):
        new_matrix[i, j] = None

count = 0
flag = 0

initial_height = 3626
final_height = 7252

initial_width = 2681
final_width = 5362


def assign_color(community_id):
    color = plt.cm.tab20(community_id)

    return tuple(int(c * 255) for c in color[:3])


# matrix core
for y in range(initial_height + 1, final_height - 1):
    for x in range(initial_width + 1, final_width - 1):
        pixel = img_array[y, x]
        if not np.isnan(pixel):
            if abs(pixel) < 1000000:
                neighbors = img_array[y - 1:y + 2, x - 1:x + 2]
                count = np.count_nonzero(neighbors == pixel) - 1
                if count != 8:
                    new_matrix[y][x] = pixel

# upper line
for x in range(initial_width + 1, final_width - 1):
    pixel = img_array[initial_height, x]
    if not np.isnan(pixel):
        if abs(pixel) < 1000000:
            neighbors = img_array[initial_height:initial_height + 2, x - 1:x + 2]
            if np.all(neighbors == pixel):
                flag = 1

            if flag == 0:
                new_matrix[initial_height, x] = pixel

    flag = 0

# right line
for y in range(initial_height + 1, final_height - 1):
    pixel = img_array[y, final_width - 1]
    if not np.isnan(pixel):
        if abs(pixel) < 1000000:
            neighbors = img_array[y - 1:y + 2, final_width - 2:final_width]
            if np.all(neighbors == pixel):
                flag = 1

            if flag == 0:
                new_matrix[y, final_width - 1] = pixel

    flag = 0

# bottom line
for x in range(initial_width + 1, final_width - 1):
    pixel = img_array[final_height - 1, x]
    if not np.isnan(pixel):
        if abs(pixel) < 1000000:
            neighbors = img_array[final_height - 2:final_height, x - 1:x + 2]
            if np.all(neighbors == pixel):
                flag = 1

            if flag == 0:
                new_matrix[final_height - 1, x] = pixel

    flag = 0

# left line
for y in range(initial_height + 1, final_height - 1):
    pixel = img_array[y, initial_width]
    if not np.isnan(pixel):
        if abs(pixel) < 1000000:
            neighbors = img_array[y - 1:y + 2, initial_width:initial_width + 2]
            if np.all(neighbors == pixel):
                flag = 1

            if flag == 0:
                new_matrix[y, initial_width] = pixel

    flag = 0

# upper left corner
pixel = img_array[initial_height, initial_width]
if not np.isnan(pixel) and np.all(
        pixel == img_array[initial_height:initial_height + 2, initial_width:initial_width + 2]):
    flag = 1
else:
    if abs(pixel) < 1000000:
        new_matrix[initial_height, initial_width] = pixel
        flag = 0

# upper right corner
pixel = img_array[initial_height, final_width - 1]
if not np.isnan(pixel) and np.all(pixel == img_array[initial_height:initial_height + 2, final_width - 2:final_width]):
    flag = 1
else:
    if abs(pixel) < 1000000:
        new_matrix[initial_height, final_width - 1] = pixel
        flag = 0

# bottom right corner
pixel = img_array[final_height - 1, final_width - 1]
if not np.isnan(pixel) and np.all(pixel == img_array[final_height - 2:final_height, final_width - 2:final_width]):
    flag = 1
else:
    if abs(pixel) < 1000000:
        new_matrix[final_height - 1, final_width - 1] = pixel
        flag = 0

# bottom left corner
pixel = img_array[final_height - 1, initial_width]
if not np.isnan(pixel) and np.all(pixel == img_array[final_height - 2:final_height, initial_width:initial_width + 2]):
    flag = 1
else:
    if abs(pixel) < 1000000:
        new_matrix[final_height - 1, initial_width] = pixel
        flag = 0

# print('------------------')
# print(img_array)
# print('------------------')
# print(new_matrix)
# print('------------------')


graph = nx.Graph()
for y in range(final_height):
    for x in range(final_width):
        pixel = new_matrix[y, x]
        if not np.isnan(pixel):
            if abs(pixel) < 1000000:
                graph.add_node((y, x, pixel))

print('-------- Grafo: ---------')
print(graph)
# print(graph.nodes)

# --------------------------------------- adding egdes ---------------------------------------

# matrix core
for y in range(initial_height + 1, final_height - 1):
    for x in range(initial_width + 1, final_width - 1):
        pixel = new_matrix[y, x]
        if not np.isnan(pixel):
            neighbors = [
                (y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1),
                (y - 1, x - 1), (y - 1, x + 1), (y + 1, x - 1), (y + 1, x + 1)
            ]
            for ny, nx in neighbors:
                neighbor_pixel = new_matrix[ny, nx]
                if pixel != neighbor_pixel and not np.isnan(neighbor_pixel):
                    graph.add_edge((y, x, pixel), (ny, nx, neighbor_pixel))

# upper line
for x in range(initial_width + 1, final_width - 1):
    pixel = new_matrix[initial_height, x]
    if not np.isnan(pixel):
        neighbors = [(initial_height, x - 1), (initial_height, x + 1), (initial_height + 1, x - 1),
                     (initial_height + 1, x), (initial_height + 1, x + 1)]
        for ny, nx in neighbors:
            neighbor_pixel = new_matrix[ny, nx]
            if not np.isnan(neighbor_pixel) and pixel != neighbor_pixel:
                graph.add_edge((initial_height, x, pixel), (ny, nx, neighbor_pixel))

# right line
for y in range(initial_height + 1, initial_height - 1):
    pixel = new_matrix[y, final_width - 1]
    if not np.isnan(pixel):
        neighbors = [(y + 1, final_width - 1), (y - 1, final_width - 2), (y - 1, final_width - 1),
                     (y + 1, final_width - 2), (y, final_width - 2)]
        for ny, nx in neighbors:
            neighbor_pixel = new_matrix[ny, nx]
            if not np.isnan(neighbor_pixel) and pixel != neighbor_pixel:
                graph.add_edge((y, final_width - 1, pixel), (ny, nx, neighbor_pixel))

# bottom line ------------- ERROR ------------
for x in range(initial_width + 1, final_width - 1):
    pixel = new_matrix[final_height - 1, x]
    if not np.isnan(pixel):
        neighbors = [(final_height - 1, x - 1), (final_height - 1, x + 1), (final_height - 2, x - 1),
                     (final_height - 2, x + 1), (final_height - 2, x)]
        for ny, nx in neighbors:
            neighbor_pixel = new_matrix[ny, nx]
            if not np.isnan(neighbor_pixel) and pixel != neighbor_pixel:
                graph.add_edge((final_height - 1, x, pixel), (ny, nx, neighbor_pixel))

# left line
for y in range(initial_height + 1, final_height - 1):
    pixel = new_matrix[y, initial_width]
    if not np.isnan(pixel):
        neighbors = [(y - 1, initial_width), (y + 1, initial_width), (y - 1, initial_width + 1),
                     (y + 1, initial_width + 1), (y, initial_width + 1)]
        for ny, nx in neighbors:
            neighbor_pixel = new_matrix[ny, nx]
            if not np.isnan(neighbor_pixel) and pixel != neighbor_pixel:
                graph.add_edge((y, initial_width, pixel), (ny, nx, neighbor_pixel))

# upper left corner
pixel = new_matrix[initial_height, initial_width]
if not np.isnan(pixel):
    neighbors = [(initial_height + 1, initial_width), (initial_height, initial_width + 1),
                 (initial_height + 1, initial_width + 1)]
    for ny, nx in neighbors:
        neighbor_pixel = new_matrix[ny, nx]
        if not np.isnan(neighbor_pixel) and pixel != neighbor_pixel:
            graph.add_edge((initial_height, initial_width, pixel), (ny, nx, neighbor_pixel))

# upper right corner
pixel = new_matrix[initial_height, final_width - 1]
if not np.isnan(pixel):
    neighbors = [(initial_height, final_width - 2), (initial_height + 1, final_width - 1),
                 (initial_height + 1, final_width - 2)]
    for ny, nx in neighbors:
        neighbor_pixel = new_matrix[ny, nx]
        if not np.isnan(neighbor_pixel) and pixel != neighbor_pixel:
            graph.add_edge((initial_height, final_width - 1, pixel), (ny, nx, neighbor_pixel))

# bottom right corner
pixel = new_matrix[final_height - 1, final_width - 1]
if not np.isnan(pixel):
    neighbors = [(final_height - 1, final_width - 2), (final_height - 2, final_width - 1),
                 (final_height - 2, final_width - 2)]
    for ny, nx in neighbors:
        neighbor_pixel = new_matrix[ny, nx]
        if not np.isnan(neighbor_pixel) and pixel != neighbor_pixel:
            graph.add_edge((final_height - 1, final_width - 1, pixel), (ny, nx, neighbor_pixel))

# bottom left corner
pixel = new_matrix[final_height - 1, initial_width]
if not np.isnan(pixel):
    neighbors = [(final_height - 1, initial_width + 1), (final_height - 2, initial_width),
                 (final_height - 2, initial_width + 1)]
    for ny, nx in neighbors:
        neighbor_pixel = new_matrix[ny, nx]
        if not np.isnan(neighbor_pixel) and pixel != neighbor_pixel:
            graph.add_edge((final_height - 1, initial_width, pixel), (ny, nx, neighbor_pixel))

print(graph)

print('-------- Clustering: ---------')

partition = community.best_partition(graph)

for node, community_id in partition.items():
    graph.nodes[node]['community'] = community_id

dict_values = partition.values()
max_value = max(dict_values)

communities = np.zeros(max_value + 1, dtype=int)
for community_id in partition.values():
    communities[community_id] += 1

for i in range(max_value + 1):
    print(
        f"A comunidade {i} possui {communities[i]} nós o que"
        f" representa {(communities[i] * 100) / graph.number_of_nodes()}% do grafo")
print('----------------------------------------------------------------------------------------')

# for node, data in graph.nodes(data=True):
#     print(f"O nó {node} pertence a comunidade {data['community']}")

# for q in range(final_height):
#     for w in range(final_width):
#         community_id = partition.get((q, w, new_matrix[q, w]))
#         if community_id is not None:
#             color = assign_color(community_id)
#             community_image[q, w] = color

community_values = {i: [] for i in range(max_value + 1)}

for node, community_id in partition.items():
    _, _, pixel_value = node
    community_values[community_id].append(pixel_value)

differences = {}
for community_id, values in community_values.items():
    min_value = min(values)
    max_value = max(values)
    difference = max_value - min_value
    differences[community_id] = difference

sorted_communities = sorted(differences.items(), key=lambda item: item[1], reverse=True)

top_3_communities = sorted_communities[:3]
print("As 3 comunidades com as maiores diferenças são:")
for community_id, difference in top_3_communities:
    print(f"Comunidade {community_id} com diferença de {difference}")



print('----------------------------------------------------------------------------------------')
for community_id, _ in top_3_communities:
    values = community_values[community_id]
    mean_value = np.mean(values)
    median_value = np.median(values)
    std_deviation = np.std(values)

    print(f"Comunidade {community_id}:")
    print(f"Valores: {values}")
    print(f"Valor mínimo: {min(values)}")
    print(f"Valor máximo: {max(values)}")
    print(f"Média: {mean_value}")
    print(f"Mediana: {median_value}")
    print(f"Desvio padrão: {std_deviation}")
    print('----------------------------------------------------------------------------------------')

gray = (128, 128, 128)
black_image = np.full((7252, 5362, 3), gray, dtype=np.uint8)

for (y, x, pixel), community_id in partition.items():
    if community_id in [cid for cid, _ in top_3_communities]:
        color = assign_color(community_id)
        black_image[y, x] = color

community_image_pil = Image.fromarray(black_image)
community_image_pil.show()
community_image_pil.save('top_5_communities_declividade_image_IV.png')

# community_image_pil = Image.fromarray(community_image)
#
# community_image_pil.show()
# community_image_pil.save('community_image.png')

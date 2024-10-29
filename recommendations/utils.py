from math import radians
from sklearn.metrics.pairwise import haversine_distances
from itertools import permutations
def get_distance_matrix(places):
    # In case of real scenario, Google's Distance Martrix API is more accurate and real-time
    lat_long = [[radians(place.latitude),(radians(place.longitude))] for place in places]
    distance_matrix = haversine_distances(lat_long) * 6371
    
    # keys = []
    # values = []
    # for i in range(len(places)):
    #     for j in range(len(places)):
    #         if i != j:
    #             keys.append((places[i].name, places[j].name))
    #             values.append(distance_matrix[i][j])
    # pairwise_distance_dict = dict(zip(keys,values))
    return distance_matrix

def get_pairwise_dict(distances):
    pairwise_dict = {}
    for i in range(len(distances)):
         for j in range(len(distances)):
             if i != j:
                 pairwise_dict[(i,j)] = distances[i][j]
    return pairwise_dict

def calculate_cost(distance_matrix, route):
    distance = 0
    # pairwise_dict = get_pairwise_dict(distances=distances)
    n = len(route)
    for i in range(n-1):
        distance += distance_matrix[route[i]][route[i+1]]
        # print(f"from {route[i]} to {route[i+1]}")
    # Add the back route
    distance += distance_matrix[route[n-1]][route[0]]
    # print(f"from {route[n-1]} to {route[0]}")
    return distance
def get_min_distance(places):
    
    # get distance matrix
    distance_matrix = get_distance_matrix(places)
    sorted_places = []
    # print([i for i in range(len(places))])
    all_permutations = permutations([i for i in range(len(places))])
    min_distance = float('inf')
    optimal_route = []

    # if len(places) < 4:
    for perm in all_permutations:
        distance = calculate_cost(distance_matrix, perm)

        if distance < min_distance:
            min_distance = distance
            optimal_route = list(perm) + [perm[0]]
            # sorted_places = route
    # print(places[0].)
    sorted_places = [{"id":places[i].id, "name":places[i].name, } for i in optimal_route]
        

    return min_distance, sorted_places
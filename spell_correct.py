import numpy as np

Prefix_completion_cost = 0.2


def get_prefix_distance(input_string, candidate_string):
    input_string = input_string.lower()
    prefix_len = len(input_string)

    candidate_string = candidate_string.lower()[:prefix_len] #truncating if characters are present in candidate string
    candidate_len = len(candidate_string)

    row_num = prefix_len + 1
    col_num = candidate_len + 1

    distance_matrix = np.zeros((row_num, col_num))

    distance_matrix[0, 1:] = [x for x in range(1, col_num)] #filling first row
    distance_matrix[1:, 0] = [x for x in range(1, row_num)] #filling first column

    for i in range(1, row_num):
        for j in range(1, col_num):
            if input_string[i-1] == candidate_string[j-1]:
                distance_matrix[i, j] = distance_matrix[i-1, j-1]
            else:
                distance_matrix[i, j] = min(distance_matrix[i-1,j-1],
                                            distance_matrix[i-1,j],
                                            distance_matrix[i,j-1]) + 1
    #print(distance_matrix)
    return distance_matrix[-1,-1] #value in the bottom right corner


def get_insert_distance(input_string, candidate_string):
    insert_ops = len(candidate_string) - len(input_string) #output_length-j
    return Prefix_completion_cost*insert_ops # p_c_c*(output_length-j)


def get_edit_distance(input_string, candidate_string):
    pdistance = get_prefix_distance(input_string, candidate_string)
    idistance = get_insert_distance(input_string, candidate_string)    
    return pdistance + idistance #unit cost for prefix and reduced cost for insertion


def get_candidates_with_distance(query, candidates): #query - word to be auto-completed/corrected.
                                                     #candidates-list of all personlised words
    rank = {}

    for candidate in candidates:
        edist = get_edit_distance(query, candidate) #edit distance between query term and candidate

        if rank.get(edist):
            rank[edist].append(candidate)
        else:
            rank[edist] = [candidate]
   # print(rank)

    return rank


def generate_rank(query, candidates):
    result = get_candidates_with_distance(query, candidates)
    ranked_candidates = [] #to store final result
        
    for k in sorted(list(result.keys())):
        ranked_candidates=ranked_candidates+list(result[k])

    return ranked_candidates[0:6] #return top 6 results 

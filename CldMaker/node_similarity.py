import itertools

import numpy as np
import tensorflow_hub as hub

embed = hub.load("")

def list_to_sentence(node_list):
    sentence = ' '.join(map(str,node_list))
    return sentence

def get_all_orders(nodes_list):
    combination_list = get_all_orders(nodes_list)
    sentence = list_to_sentence(nodes_list)
    embeddings = embed([sentence])
    result = np.empty(embeddings.shape)

    for i in range(len(combination_list)):
        nodes_list = combination_list[i]
        sentence = list_to_sentence(nodes_list)
        embeddings = embed([sentence])
        result = np.concatenate((result,embeddings),axis = 0)

    final_result = np.delete(result,0,0)
    average_emb = np.mean(final_result,axis = 0)
    return average_emb

def cosine_similarity(v1,v2):
    mag1 = np.linalg.norm(v1)
    mag2 = np.linalg.norm(v2)
    if (not mag1) or (not mag2):
        return 0
    return np.dot(v1,v2)/(mag1 *mag2)

def get_semantic_similarity_nodes(g1_node_list, g2_node_list):
    g1_sentence = list_to_sentence(g1_node_list)
    g2_sentence = list_to_sentence(g2_node_list)

    g1_embeddings = embed([g1_sentence])
    g2_embeddings = embed([g2_sentence])

    similarity_score = cosine_similarity(
        g1_embeddings, np.transpose(g2_embeddings)
    )[0][0]

    return similarity_score
import numpy as np
import tensorflow_hub as hub

from cld_properties import CLD, get_graph_distance
from node_similarity import get_semantic_similarity_nodes

embed = hub.load('https://tfhub.dev/google/universal-sentence-encoder/4')


def get_eval_metrics(df):
    for index, row in df.iterows():
        label_graph = CLD(row['nx_label_graph'])
        df.loc[index, 'label_nodes'] = label_graph.number_of_nodes()
        df.loc[index, 'label_links'] = label_graph.number_of_links()
        df.loc[index, 'label_r_loops'] = label_graph.get_num_r_loop()
        df.loc[index, 'label_b_loops'] = label_graph.get_num_b_loop()

        predicted_graph = CLD(row['nx_extracted_graph'])
        df.loc[index, 'predicted_nodes'] = predicted_graph.number_of_nodes()
        df.loc[index, 'predicted_links'] = predicted_graph.number_of_links()
        df.loc[index, 'predicted_r_loops'] = predicted_graph.get_num_r_loop()
        df.loc[index, 'predicted_b_loops'] = predicted_graph.get_num_b_loop()

        df.loc[index, 'semantic_variable_score'] = get_semantic_similarity_nodes(label_graph, predicted_graph)
        df.loc[index, 'GED_score'] = get_graph_distance(label_graph, predicted_graph)

    df['pt_nodes'] = (df['predicted_nodes'] - df['label_nodes']) / df['label_nodes']
    df['pt_links'] = (df['predicted_links'] - df['label_links']) / df['label_links']
    df['pt_r_loop'] = (df['predicted_r_loops'] - df['label_r_loops']) / df['label_r_loops']
    df['pt_b_loop'] = (df['predicted_b_loops'] - df['label_b_loops']) / df['label_b_loops']

    df.fillna(0, replace=True)

    df.replace(np.inf, 1, inplace=True)
    return df

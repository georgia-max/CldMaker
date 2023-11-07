
import os
import json
from pprint import pprint
from typing import List, Dict, Tuple, Any, Optional, Union
import glob
from IPython.display import display
import ipywidgets as widgets

import numpy as np
import pandas as pd
import networkx as nx
import graphviz
# import tensorflow as tf
# tf.compat.v1.enable_eager_execution()

import langchain
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate
#from langchain.llms import VertexAI
from langchain.llms import OpenAI
from langchain.chains import LLMChain, TransformChain, SequentialChain
from langchain.evaluation.criteria.eval_chain import CriteriaEvalChain

import graphviz_analysis as ga 
import prompts as pr
from graphviz_analysis import render_gvz, clean_graphs, check_syntax
from print_result import print_result_docx



# One stage appraoch 
config_v2=[
    {
        'input_variables':['dynamic_hypothesis'],
        'output_variables':['label_graphs'],
        'prompt_prefix':'''
       
        '''
    }
]
# One stage appraoch 
config_v3 =[
    {
        'input_variables':['dynamic_hypothesis'],
        'output_variables':['label_graphs'],
        'prompt_prefix':'''
        
        First, Render a list of variable names from the text given.
        The variable names shuold be nouns or nouns phrases. 
        The variable names should have a sense of directionality. Chose names for which the 
        the meaning of an increase or decrease is clear. 

        Second, Render a dot format based on the variable names.
        A positive relationship is indicated by an arrow from the first variable to the second variable with the sign [vee]. 
        A negative relationship is indicated by an arrow from the first variable to the second variable with the sign [tee].
        '''
    }
]

# Second stage appraoch

config =[
    {
        'input_variables':['dynamic_hypothesis'],
        'output_variables':['variables'],
        'prompt_prefix':'''
        Render a list of variable names from the text given. Following the rules below: 

        1. The variable names should be nouns or nouns phrases. 
        2. The variable names should have a sense of directionality. 
        '''
    },
    {
        'input_variables':['variables','dynamic_hypothesis'],
        'output_variables':['label_graphs'],
        'prompt_prefix':'''
        Render a dot format of variable names from the text given. Following the steps below:

        Step 1. Identify the relative pairs among the given variable names and the dynamic hypothesis. 
        Step 2. Identify whether the cause-effect relationship between the relative pairs is positive or negative.
        Step 3. A positive relationship is indicated by [arrowhead=vee]. A negative relationship is indicated [arrowhead=tee].
        Step 4. Create a DOT format based on the variable names and the cause-effect relationship. The DOT format starts with: digraph {}
        '''
    }
]

config_v4=[
    {
        'input_variables':['dynamic_hypothesis'],
        'output_variables':['variables'],
        'prompt_prefix':'''
        Render a list of variable names from the text given. Following the rules below:=
        1. The variable names should be nouns or nouns phrases. 
        2. The variable names should have a sense of directionality. 
        '''
    },
    {
        'input_variables':['variables','dynamic_hypothesis'],
        'output_variables':['label_graphs'],
        'prompt_prefix':'''
        The variables' names will be rendered in DOT format. The steps are as follows:
        Step 1: Identify the cause-effect relationship between variable names given the dynamic hypothesis.
        Step 2: [arrowhead=vee] indicates a positive relationship. A negative relationship is indicated by [arrowhead=tee].
        Step 3: Create a DOT format based on the cause-effect relationship.
        '''
    }
]

def read_dataset(path: str):
    """
    Reads the dataset from the given path. 
    """
    # df = pd.read_csv(path, index_col= 0, dtype= 'str')
    df = pd.read_json(path)
    return df

def cld_maker(my_variables:"str", my_hypothesis:"str"): 

    prompts_df = read_dataset('/Users/Georgia 1/CldMaker-1/CldMaker/prompt_dict.json')

    prompts_df['label_graphs'] = prompts_df['label_graphs'].str.replace(
        '{','{{',regex = False
    ).str.replace(
        '}','}}',regex = False
    )

    prompts_df['dynamic_hypothesis'] = prompts_df['dynamic_hypothesis'].str.strip('\n').str.strip(' ')

    from sklearn.model_selection import train_test_split
    train_df, test_df = train_test_split(prompts_df, test_size = 80/100.0,
                                        shuffle=False)


    llm = OpenAI(temperature=0, openai_api_key = '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')


    full_chain = pr.make_few_shot_sequential_chain(config_v3, train_df, llm)

    result = full_chain.run({"variables":my_variables, 
                         "dynamic_hypothesis":my_hypothesis})


    clean_result = clean_graphs(result)


    return str(clean_result)

# results_df = cld_maker(prompts_df)

# display(results_df.head(3)) 

# print(results_df.head(3))
# for ind in results_df.index:

#     print("Case ", ind)
#     g_label = results_df['label_graphs'][ind]
#     ga.render_gvz(g_label, ind,"label", "version4")

#     g_predict = results_df['label_graphs_out'][ind]
#     ga.render_gvz(g_predict, ind,"predict", "version4")

#     print("-----------------------------------------")


# print_result_docx("Results_version4", "img/version4/", "outputs/Result_version4", results_df)





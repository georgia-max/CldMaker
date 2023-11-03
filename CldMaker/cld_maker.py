import os

import pandas as pd
from langchain.llms import OpenAI

import CldMaker.prompts as pr
from CldMaker.graphviz_analysis import clean_graphs

# One stage approach
config_v2 = [
    {
        'input_variables': ['dynamic_hypothesis'],
        'output_variables': ['label_graphs'],
        'prompt_prefix': '''
       
        '''
    }
]
# One stage appraoch 
config_v3 = [
    {
        'input_variables': ['dynamic_hypothesis'],
        'output_variables': ['label_graphs'],
        'prompt_prefix': '''
        
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

# config =[
#     {
#         'input_variables':['dynamic_hypothesis'],
#         'output_variables':['variables'],
#         'prompt_prefix':'''
#         Render a list of variable names from the text given. Following the rules below: 

#         1. The variable names should be nouns or nouns phrases. 
#         2. The variable names should have a sense of directionality. 
#         '''
#     },
#     {
#         'input_variables':['variables','dynamic_hypothesis'],
#         'output_variables':['label_graphs'],
#         'prompt_prefix':'''
#         Render a dot format of variable names from the text given. Following the steps below:

#         Step 1. Identify the relative pairs among the given variable names and the dynamic hypothesis. 
#         Step 2. Identify whether the cause-effect relationship between the relative pairs is positive or negative.
#         Step 3. A positive relationship is indicated by [arrowhead=vee]. A negative relationship is indicated [arrowhead=tee].
#         Step 4. Create a DOT format based on the variable names and the cause-effect relationship. The DOT format starts with: digraph {}
#         '''
#     }
# ]


class GraphGenerator:
    def __init__(self, openai_api_key: str):
        self.project_root = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
        self.prompts_df = self.read_dataset(os.path.join(self.project_root, 'prompt_dict.json'))
        self.llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
        self.config_v4 = [
            {
                'input_variables': ['dynamic_hypothesis'],
                'output_variables': ['variables'],
                'prompt_prefix': '''
                    Render a list of variable names from the text given. Following the rules below:=
                    1. The variable names should be nouns or nouns phrases. 
                    2. The variable names should have a sense of directionality. 
                '''
            },
            {
                'input_variables': ['variables', 'dynamic_hypothesis'],
                'output_variables': ['label_graphs'],
                'prompt_prefix': '''
                    The variables' names will be rendered in DOT format. The steps are as follows:
                    Step 1: Identify the cause-effect relationship between variable names given the dynamic hypothesis.
                    Step 2: [arrowhead=vee] indicates a positive relationship. A negative relationship is indicated by [arrowhead=tee].
                    Step 3: Create a DOT format based on the cause-effect relationship.
                '''
            }
        ]

    @staticmethod
    def read_dataset(file_path: str):
        """
        Reads the dataset from the given path.
        """
        return pd.read_json(file_path)

    def generate_by_hypothesis(self, my_hypothesis: "str"):
        self.format_prompt()

        full_chain = self.make_few_shot_sequential_chain(self.prompts_df)
        result = full_chain.run({
            "variables": "",
            "dynamic_hypothesis": my_hypothesis
        })

        clean_result = clean_graphs(result)

        return str(clean_result)

    def format_prompt(self):
        self.prompts_df['label_graphs'] = self.prompts_df['label_graphs'].str.replace(
            '{', '{{', regex=False
        ).str.replace(
            '}', '}}', regex=False
        )
        self.prompts_df['dynamic_hypothesis'] = self.prompts_df['dynamic_hypothesis'].str.strip('\n').str.strip(' ')

    def make_few_shot_sequential_chain(self, prompts_df):
        from sklearn.model_selection import train_test_split
        train_df, test_df = train_test_split(prompts_df, test_size=80 / 100.0, shuffle=False)
        full_chain = pr.make_few_shot_sequential_chain(self.config_v4, train_df, self.llm)
        return full_chain

import langchain
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate
#from langchain.llms import VertexAI
from langchain.llms import OpenAI
from langchain.chains import LLMChain, TransformChain, SequentialChain
from langchain.evaluation.criteria.eval_chain import CriteriaEvalChain

from typing import List, Dict, Tuple, Any, Optional, Union
import pandas as pd

config =[
    {
        'input_variables':['dynamic_hypothesis'],
        'output_variables':['variables'],
        'prompt_prefix':'''
        Render a list of variable names from the text given.

        The variable names in
        '''
        ###Write up
    },
    {
        'input_variables':['variables','dynamic_hypothesis'],
        'output_variables':['label_graphs'],
        'prompt_prefix':'''
        Render a dot format of variable names from the text given.


        '''
        ###Write up
    }
]

def make_few_shot_prompt(
    input_variables: List[str],
    output_variables:List[str],
    prompt_prefix: str,
    examples_df: pd.DataFrame,
    variable_delimiter: str,
)-> FewShotPromptTemplate:

  all_variables = input_variables+ output_variables

  few_shot_prompt = FewShotPromptTemplate(
      examples = examples_df[all_variables].to_dict('records'),
      example_prompt = PromptTemplate(
          input_variables=all_variables,
          template = f'{variable_delimiter}\n'.join([f'{v}:{{{v}}}'
                                                  for v in all_variables]),
      ),
      prefix = prompt_prefix,
      suffix = f'{variable_delimiter}\n'.join([f'{v}:{{{v}}}'for v in input_variables]),
      input_variables = input_variables,
  )
  return few_shot_prompt

def make_few_shot_sequential_chain(
    config: List[Dict[str, Union[List[str],str]]],
    examples_df: pd.DataFrame,
    llm: langchain.llms.base.LLM,
    variable_delimiter: str ='|||'
) -> SequentialChain:

  chain_elements = []
  all_output_variables =[]
  for stage_info in config:
    input_variables = stage_info['input_variables']
    output_variables = stage_info['output_variables']
    prompt_prefix = stage_info['prompt_prefix']

    prompt = make_few_shot_prompt(input_variables,
                                  output_variables,
                                  prompt_prefix,
                                  examples_df,
                                  variable_delimiter
                                  )

  # LLM is MISO. To make the each stage MIMO, we create a SequentialChain from
  # the said LLMChain and a follow uup TransformChain that extracts the output
  # variables from the LLMChain's output. Using an output parser did not work because
  # the LLMChain can ultimately just return  one output.

  def transform_func(inputs: Dict)-> Dict:
    actual_vars_formatted = []
    actual_vars_unformatted = inputs['text'].split(variable_delimiter)
    for actual_var in actual_vars_unformatted:
      if ':' in actual_var:
        var_name, var_value = tuple(actual_var.split(':',1))
        var_name = var_name.strip('\n').strip()
        var_value = var_value.strip('\n').strip()
        actual_vars_formatted.append((var_name, var_value))
    return dict(actual_vars_formatted)

  chain_element = SequentialChain(
      input_variables = input_variables,
      output_variables = output_variables,
      chains = [
          LLMChain(prompt = prompt, llm=llm),
          TransformChain(
              input_variables=['text'],output_variables=output_variables,
              transform= transform_func
            )
      ]
  )

  chain_elements.append(chain_element)
  all_output_variables.extend(output_variables)

  full_chain = SequentialChain(
      chains = chain_elements,
      input_variables=chain_elements[0].input_variables,
      output_variables=all_output_variables,
  )
  return full_chain

def apply_chain_on_df(chain: SequentialChain,
                      df: pd.DataFrame,
                      output_suffix: str = '_out') -> pd.DataFrame:

    results_df = pd.DataFrame(
        [chain(row[chain.input_variables].to_dict())
        for _,row in df.iterrows()],
        index = df.index,
    )
    results_df = results_df[chain.output_variables]
    results_df.columns = results_df.columns + f'{output_suffix}'
    return results_df

# def get_df_from_sheet_url(url:str,sheet_name) -> pd.DataFrame:
#   rows = gc.open_by_url(url)
#   worksheet = rows.worksheet(sheet_name)

#   df = pd.DataFrame(worksheet.get_all_records())
#   return df
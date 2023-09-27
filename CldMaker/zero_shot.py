import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import json
import pandas as pd


class ZeroShotUtility:
    def __init__(self, template, temperature=0):
        self.template = template
        self.temperature = temperature

    def __str__(self):
        return f"{self.template}"

    def print_cld(self, dynamic_h):
        prompt_template = ChatPromptTemplate.from_template(self.template)
        message = prompt_template.format_messages(dynamic_h =dynamic_h)
        llm = ChatOpenAI(temperature=self.temperature, 
                         openai_api_key="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")
        response = llm(message)
        print(response.content)
        print("------------------------------------------------------------")
        return response.content

def get_prompt_template():
    return """
    
    I want you to play the role of a system dynamics modeler.

    Given a dynamic hypothesis, what is the casual loop diagram?
    Return the answer in a text format.
    
    Dynamic Hypothesis: {dynamic_h}
    """

if __name__ == '__main__':
    prompt_template = get_prompt_template()

    zeroShot = ZeroShotUtility(template=prompt_template)

    prompts_df = pd.read_csv('CldMaker/dataset/prompts_vars.csv', index_col= 0, dtype= 'str')
    
    # file1 = open("CldMaker/outputs/zeroshot.txt","w")

    # for ind in prompts_df.index:
    #     dynamic_h = prompts_df.loc[ind, 'dynamic_hypothesis']
    #     print("case", ind)
    #     response = zeroShot.print_cld(dynamic_h=dynamic_h)
    #     file1.write(response + '\n')
    
    # file1.close()
    
    # dynamic_h = get_dynamic_h()
    dynamic_h = """a larger population leads to a higher number of births, 
                and higher births leads to a higher populatioh. 
                The larger population will tend to have a greater number of deaths. """
    zeroShot.print_cld(dynamic_h=dynamic_h)
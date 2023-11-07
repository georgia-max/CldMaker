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

    Given a dynamic hypothesis, please provide the casual loop diagram?
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
    dynamic_h = """
        The Assignment Backlog is increased by the Assignment Rate and decreased by the Completion Rate. 
        Completion Rate is Workweek (hours per week) times Productivity (tasks completed per hour of effort) times the Effort Devoted to Assignments. 
        Effort Devoted to Assignments is the effort put in by the student compared to the effort required to complete the assignment with high quality. 
        If work pressure is high, the student may choose to cut corners, skim some reading, skip classes, or give less complete answers to the questions in assignments. 
        For example, if a student works 50 hours per week and can do one task per hour with high quality but only does half the work each assignment requires for a good job, 
        then the completion rate would be (50)(1)(.5) = 25 task equivalents per week.

        Work Pressure determines the workweek and effort devoted to assignments. 
        Work pressure depends on the assignment backlog and the Time Remaining to complete the work: The bigger the backlog or the less time remaining,
        the higher the workweek needs to be to complete the work on time. Time remaining is of course simply the difference between the Due Date and the current Calendar Time. 
        The two most basic options available to a student faced with high work pressure are to first, work longer hours, thus increasing the completion rate and reducing the backlog , 
        or second, work faster by spending less time on each task, speeding the completion rate and reducing the backlog. Both are negative feedbacks whose goal 
        is to reduce work pressure to a tolerable level.
                """
    zeroShot.print_cld(dynamic_h=dynamic_h)
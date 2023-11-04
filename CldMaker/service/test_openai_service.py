import pandas as pd

from CldMaker.service.openai_service import OpenAIService


class TestOpenAIService:

    def setup_method(self):
        self.openai_service = OpenAIService()

        d = [{
            "dynamic_hypothesis": "\nThe order rate decision\n",
            "label_graphs": "digraph {{\n\"order rate\" }}",
        }]
        self.raw_prompts_df = pd.DataFrame(data=d)

    def test_format_prompt_dynamic_hypothesis_field(self):
        self.openai_service.prompts_df = self.raw_prompts_df
        assert "\n" in self.openai_service.prompts_df["dynamic_hypothesis"][0]

        self.openai_service.format_prompt()

        assert self.openai_service.prompts_df["dynamic_hypothesis"][0] == "The order rate decision"

    def test_format_prompt_label_graphs_field(self):
        self.openai_service.prompts_df = self.raw_prompts_df

        self.openai_service.format_prompt()

        assert self.openai_service.prompts_df["label_graphs"][0] == "digraph {{{{\n\"order rate\" }}}}"

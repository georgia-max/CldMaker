from CldMaker.graphviz_analysis import clean_graphs


class GraphGenerator:
    def __init__(self, llm_service):
        self.llm_service = llm_service

    def generate_by_hypothesis(self, my_hypothesis: "str"):
        result = self.llm_service.run_full_chain({
            "variables": "",
            "dynamic_hypothesis": my_hypothesis
        })

        clean_result = clean_graphs(result)

        return str(clean_result)

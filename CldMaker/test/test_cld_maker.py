from unittest.mock import Mock

from CldMaker.cld_maker import GraphGenerator


class TestGraphGenerator:
    def setup_method(self):
        self.openai_service = Mock()
        self.openai_service.run_full_chain.return_value = """
            digraph {
                ""order rate"" -> ""inventory"" [arrowhead = vee]
                ""inventory""->""order rate""[arrowhead = tee] 
                ""desired inventory"" -> ""order rate""[arrowhead = vee] 
                ""adjustment time"" -> ""order rate""[arrowhead = tee] 
            }"
        """
        self.generator = GraphGenerator(self.openai_service)

    def test_llm_service_called_once(self):
        self.generator.generate_by_hypothesis("test")
        assert self.openai_service.run_full_chain.call_count == 1

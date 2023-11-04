from repository.opinion import OpinionRepository


class TestCreateOpinion:

    def setup_method(self):
        self.repo = OpinionRepository()

    def teardown_method(self):
        self.repo.truncate_table()

    def test_create_opinion(self):
        opinion_id = self.repo.create_opinion(
            "Test User Input Opinion", "Test Predicted Var", "Test Predicted Graph")

        res = self.repo.read_opinion(opinion_id)
        assert res is not None

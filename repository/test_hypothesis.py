from app import app
from repository.hypothesis import HypothesisRepository


class TestCreateHypothesis:

    def setup_method(self):
        self.repo = HypothesisRepository()

    def teardown_method(self):
        self.repo.truncate_table()

    def test_create_hypothesis(self):
        with app.app_context():
            hypothesis = self.repo.create_hypothesis(
                "Test User Input Hypothesis", "Test Predicted Var", "Test Predicted Graph")

            # res = Hypothesis.query.all()
            res = self.repo.read_hypothesis(hypothesis.id)
            assert res is not None

from unittest import mock

import pytest

from main import app
from repository.opinion import OpinionRepository


@pytest.fixture()
def client(app):
    return app.test_client()


class TestApp:
    def setup_method(self):
        self.repo = OpinionRepository()

    def teardown_method(self):
        self.repo.truncate_table()

    @mock.patch('CldMaker.cld_maker.GraphGenerator.generate_by_hypothesis')
    def test_home_route(self, mock):
        """
        Test that a valid user input is saved in the database and displayed on the page
        """
        mock.return_value = """
            digraph {{ "order rate" -> "inventory" [arrowhead = vee] "inventory"->"order rate"[arrowhead = tee] "desired inventory" -> "order rate"[arrowhead = vee] }}
            """
        client = app.test_client()
        response = client.get('/?my_hypothesis=Test Hypothesis')
        assert response.status_code == 200

        # Replace with assertions to verify that the result is displayed correctly on the page
        assert b"Result: " in response.data

        # Check if the user input and result are saved in the database
        record = self.repo.find_one_opinion_by_user_input("Test Hypothesis")  # Replace with actual implementation
        assert record is not None

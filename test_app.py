import re
from unittest import mock

import pytest

from app import app
from repository.hypothesis import HypothesisRepository


@pytest.fixture()
def client(app):
    return app.test_client()


class TestApp:
    def setup_method(self):
        self.repo = HypothesisRepository()

    def teardown_method(self):
        self.repo.truncate_table()

    @mock.patch('CldMaker.cld_maker.GraphGenerator.generate_by_hypothesis')
    def test_convert_by_post(self, mock):
        """
        Test that a valid user input is saved in the database and displayed on the page
        """
        mock.return_value = """
                    digraph {{ "order rate" -> "inventory" [arrowhead = vee] "inventory"->"order rate"[arrowhead = tee] "desired inventory" -> "order rate"[arrowhead = vee] }}
                    """
        client = app.test_client()
        response = client.post('/', data={"my_hypothesis": "Test Hypothesis"})
        assert response.status_code == 200

        # Check if the user input and result are saved in the database
        record = self.repo.find_one_hypothesis_by_user_input("Test Hypothesis")
        assert record is not None

    @mock.patch('CldMaker.cld_maker.GraphGenerator.generate_by_hypothesis')
    def test_render_graphviz(self, mock):
        """
        Test that a valid user input is converted to a graphviz image
        """
        mock.return_value = """
            digraph {{ "order rate" -> "inventory" [arrowhead = vee] "inventory"->"order rate"[arrowhead = tee] "desired inventory" -> "order rate"[arrowhead = vee] }}
            """
        client = app.test_client()

        response = client.post('/', data={"my_hypothesis": "Test Hypothesis"})

        # assert response has svg tag and 3 title html tags
        assert b"</svg>" in response.data
        assert b"<title>desired inventory</title>" in response.data
        assert b"<title>order rate</title>" in response.data
        assert b"<title>inventory</title>" in response.data

        # Define the regular expression pattern
        pattern = r'<g id="[^\"]*" class="node">'
        matches = re.findall(pattern, response.data.decode("utf-8"))
        assert len(matches) == 3  # there are 3 nodes (topics/causes) by the generated diagraph string

    @mock.patch('CldMaker.cld_maker.GraphGenerator.generate_by_hypothesis')
    def test_no_graph_can_be_created(self, mock):
        """
        Test that a respnse is returned when no graph can be created
        """
        mock.return_value = "No variables are given, so no graph can be created."
        client = app.test_client()

        response = client.post('/', data={"my_hypothesis": "Test Hypothesis no graph results"})
        
        assert response.status_code == 200
        assert b"No variables are given, so no graph can be created." in response.data

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.data, 'html.parser')
        assert bool(soup.find('div', {'class': 'alert alert-danger'}))

from models import db, Hypothesis
from util import get_connection


class HypothesisRepository:
    def __init__(self):
        self.connection = get_connection()

    def create_hypothesis(self, user_input, predicted_var, predicted_graph_str):
        hypothesis = Hypothesis(
            user_input=user_input,
            predicted_var=predicted_var,
            predicted_graph_str=predicted_graph_str
        )
        db.session.add(hypothesis)
        db.session.commit()
        return hypothesis

    def read_hypothesis(self, hypothesis_id):
        cursor = self.connection.cursor()

        try:
            cursor.execute("SELECT * FROM hypothesis WHERE id = %s", (hypothesis_id,))
            data = cursor.fetchone()
        finally:
            cursor.close()

        return data

    def find_one_hypothesis_by_user_input(self, user_input):
        cursor = self.connection.cursor()

        try:
            cursor.execute("SELECT * FROM hypothesis WHERE user_input = %s", (user_input,))
            data = cursor.fetchone()
        finally:
            cursor.close()

        return data

    def truncate_table(self):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                "TRUNCATE TABLE hypothesis"
            )
            self.connection.commit()
        finally:
            cursor.close()
            self.connection.close()

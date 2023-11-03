from util import get_connection


class OpinionRepository:
    def __init__(self):
        self.connection = get_connection()

    def create_opinion(self, user_input, predicted_var, predicted_graph_str) -> int:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                "INSERT INTO opinion (user_input, predicted_var, predicted_graph_str) "
                "VALUES (%s, %s, %s) RETURNING id",
                (user_input, predicted_var, predicted_graph_str)
            )
            record_id = cursor.fetchone()[0]
            self.connection.commit()
        finally:
            cursor.close()

        return record_id

    def read_opinion(self, opinion_id):
        cursor = self.connection.cursor()

        try:
            cursor.execute("SELECT * FROM opinion WHERE id = %s", (opinion_id,))
            data = cursor.fetchone()
        finally:
            cursor.close()

        return data

    def find_one_opinion_by_user_input(self, user_input):
        cursor = self.connection.cursor()

        try:
            cursor.execute("SELECT * FROM opinion WHERE user_input = %s", (user_input,))
            data = cursor.fetchone()
        finally:
            cursor.close()

        return data

    def truncate_table(self):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                "TRUNCATE TABLE opinion"
            )
            self.connection.commit()
        finally:
            cursor.close()
            self.connection.close()

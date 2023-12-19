import os

import graphviz
from dotenv import load_dotenv
from flask import Flask
from flask import request
from flask_migrate import Migrate

from CldMaker.cld_maker import GraphGenerator
from CldMaker.service.openai_service import OpenAIService
from models import db
from repository.hypothesis import HypothesisRepository

app = Flask(__name__)

load_dotenv(override=True)

# WEBSITE_HOSTNAME exists only in production environment
if 'WEBSITE_HOSTNAME' not in os.environ:
    # local development, where we'll use environment variables
    print("Loading config.development and environment variables from .env file.")
    app.config.from_object('azureproject.development')
else:
    # production
    print("Loading config.production.")
    app.config.from_object('azureproject.production')

app.config.update(
    SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
# Initialize the database connection
db.init_app(app)

# Enable Flask-Migrate commands "flask db init/migrate/upgrade" to work
migrate = Migrate(app, db)
# Create tables when the app starts
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    print(request.args)
    my_hypothesis = request.args.get("my_hypothesis", "")
    svg_str = ""
    if my_hypothesis:
        generator = GraphGenerator(OpenAIService())
        graph_result = generator.generate_by_hypothesis(my_hypothesis)
    else:
        graph_result = ""
    if graph_result != "":
        repo = HypothesisRepository()
        repo.create_hypothesis(my_hypothesis, "", graph_result)
        # Convert graphviz src to svg
        g_src = graphviz.Source(graph_result)
        svg_str = g_src.pipe(format="svg", encoding='utf-8')
    return (
            """<form action="" method="get">
                <label for="my_hypothesis">Please enter your dynamic hypothesis in the text box below:</label>
                <br>
    
                Hypothesis: <input type="text" name="my_hypothesis" style="height: 200px; width: 700px; ">
                <br>
                <input type="submit" value="Convert" style="margin-left: 10px;">
                
            </form>"""
            + "Result: "
            + graph_result +
            f"""
            <div class="graphviz-output">
            {svg_str}
            </div>
            """
    )


if __name__ == '__main__':
    app.run()

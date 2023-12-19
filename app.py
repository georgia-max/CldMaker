import os

import graphviz
from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_migrate import Migrate
from markupsafe import Markup

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


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')

    my_hypothesis = request.form.get("my_hypothesis", "")
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
        removed_prefix_str = svg_str[svg_str.index("<svg"):]
        final_svg_str = ''.join(removed_prefix_str.splitlines())
    return render_template('index.html', graph_result=graph_result, svg_str=Markup(final_svg_str))


if __name__ == '__main__':
    app.run()

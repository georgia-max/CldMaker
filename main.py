from flask import Flask
from flask import request

from CldMaker import cld_maker
from repository.opinion import OpinionRepository

app = Flask(__name__)


@app.route('/')
def home():
    print(request.args)
    my_hypothesis = request.args.get("my_hypothesis", "")
    if my_hypothesis:
        graph_result = cld_maker.cld_maker(my_hypothesis)
    else:
        graph_result = ""
    if graph_result != "":
        repo = OpinionRepository()
        repo.create_opinion(my_hypothesis, "", graph_result)
    return (
            """<form action="" method="get">
    
                Hypothesis: <input type="text" name="my_hypothesis" style="height: 300px ">
                <input type="submit" value="Convert" >
                
            </form>"""
            + "Result: "
            + graph_result
    )


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)

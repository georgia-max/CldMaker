from flask import Flask
from flask import request

from CldMaker import cld_maker

app = Flask(__name__)


@app.route('/')
def home():
    print(request.args)
    my_hypothesis = request.args.get("my_hypothesis", "")
    if my_hypothesis:
        result = cld_maker.cld_maker(my_hypothesis)
    else:
        result = ""
    return (
            """<form action="" method="get">
    
                Hypothesis: <input type="text" name="my_hypothesis" style="height: 300px ">
                <input type="submit" value="Convert" >
                
            </form>"""
            + "Result: "
            + result
    )


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)

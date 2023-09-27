from flask import Flask 
import cld_maker

import pandas as pd
import glob

app = Flask(__name__)

@app.route('/')
def home():
    result = cld_maker.cld_maker()
    return result

if __name__ == '__main__':
    app.run(host = "127.0.0.1", port = 8080, debug=True)
    # prompts_df = read_dataset('CldMaker/prompt_dict.json')

    # result = cld_maker.cld_maker()
    # print(result)

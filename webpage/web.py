from flask import Flask, render_template, request, redirect
from src.query_wrapper import QueryWrapper
import json

app = Flask(__name__, template_folder='./')

query_result = '/ * Framed query results * /'
query_str = ''
frame = ''
context = ''
endpoint = ''


@app.route('/')
def hello_world():
    global query_str, frame, context
    author = "Me"
    return render_template("index.html",
                           author=author,
                           query_result=query_result,
                           endpoint=endpoint,
                           query_str=query_str,
                           frame=frame,
                           context=context
                           )


@app.route('/query', methods=['POST'])
def query():
    try:
        global query_result
        ep = request.form['endpoint']
        q = request.form['query']
        f = json.loads(request.form['frame'])
        c = json.loads(request.form['context'])

        graph = QueryWrapper(ep)
        res = graph.query(q, f, c)
        query_result = json.dumps(res['@graph'], indent=2)

        return redirect('/')
    except Exception as e:
        query_result = 'Failed, please check your inputs and try again. \n %s' % str(e)
        return redirect('/')


@app.route('/example', methods=['POST'])
def example():
    global query_str, frame, context, endpoint
    no = request.form['example']

    with open('../resources/query%s.txt' % no) as f:
        query_str = f.read()
    with open('../resources/frame%s.json' % no) as f:
        frame = f.read()
    with open('../resources/context.json') as f:
        context = f.read()
    endpoint = 'http://dbpedia.org/sparql'

    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
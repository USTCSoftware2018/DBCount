from flask import Flask, request, jsonify
from SpiderMonitor import SpiderMonitor


from functools import update_wrapper
from flask import Response, current_app


app = Flask(__name__)

def search_impl(kw):
    # TODO: impl this func
    result = SpiderMonitor().spiders(keyword=kw, timeout=5)
    return result

@app.route("/search", methods=['GET'])
def search():
    # DO NOT modify this func
    kw = request.args.get('kw')
    result = search_impl(kw)
    return jsonify(result)

if __name__ == "__main__":
    app.run()

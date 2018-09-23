from flask import Flask, request, jsonify
app = Flask(__name__)

def search_impl(kw):
    # TODO: impl this func
    result = [
        {
            'title': '',
            'url': '',
            'count': 0
        }
    ]
    return result

@app.route("/search", methods=['GET'])
def search():
    # DO NOT modify this func
    kw = request.args.get('kw')
    result = search_impl(kw)
    return jsonify(result)

if __name__ == "__main__":
    app.run()
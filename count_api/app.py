from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/search", methods=['GET'])
def search():
    kw = request.args.get('kw')
    result = [
        {
            'title': '',
            'url': '',
            'count': 0
        }
    ]
    return jsonify(result)

if __name__ == "__main__":
    app.run()
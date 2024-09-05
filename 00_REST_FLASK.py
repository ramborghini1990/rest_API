from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/tasks', methods=['POST'])
def create_task():
    # Get the JSON data from the request
    
    data = request.get_json()
    
    task = {
        'id': data.get('id'),
        'title': data.get('title'),
        'description': data.get('description')
    }

    return jsonify(task), 200



if __name__ == '__main__':
    app.run(debug=True)


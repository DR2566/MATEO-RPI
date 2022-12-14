from flask import Flask, json

def get_values():
    return [{"id": 1, "message": "hello there"}]

api = Flask(__name__)

@api.route('/companies', methods=['GET'])
def get_companies():
    return json.dumps(get_values())

if __name__ == "__main__":
    api.run(host="172.20.2.190", port='1111')
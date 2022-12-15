from flask import Flask, json
import testSensor

testing = testSensor.TEST()
print(testing.test_everything())


def get_values():
    return [{"id": 1, "message": "hello there"}]

api = Flask(__name__)

@api.route('/companies', methods=['GET'])
def get_companies():
    return json.dumps(get_values())

if __name__ == "__main__":
    api.run(host="192.168.0.115", port='1111')
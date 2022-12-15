from flask import Flask, json
import testSensor

testing = testSensor.TEST()

# def get_values():
#     return [{"id": 1, "message": "hello there"}]

api = Flask(__name__)

@api.route('/test', methods=['GET'])
def get_companies():
    try:
        result = json.dumps(testing.test_everything())
    except Exception as e:
        result = json.dumps([{"message": "something went wrong"}])
    return json.dumps(result)

if __name__ == "__main__":
    api.run(host="172.20.2.190", port='1111')

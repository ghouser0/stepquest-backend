from flask import Flask, request
from functools import wraps

def deco():
    def _deco(f):
        @wraps(f)
        def __deco(*args, **kwargs):
            auth = request.headers.get("Authorization")
            if not auth:
                return "No auth token", 403

            token = auth.split(" ")
            if len(token) != 2 or token[0] != "Bearer":
                return "Malformed auth token", 401
            
            request.user_id = token[1]

            return f(*args, **kwargs)

        return __deco

    return _deco

app = Flask(__name__)

@app.route('/hello', methods=["GET", "POST"])
def hello():
    match request.method:
        case "GET":
            return "Hello, this is GET"
        case "POST":
            return "Hello, POST"
        case _:
            return "WHAT?"

@app.route("/users", methods=["POST"])
@deco()
def users_post():
    user_id = request.user_id
    if not user_id:
        return "KYS!! Keep yourself safe!", 400

    return f"POSTED UserId: {user_id}", 200

@app.route("/users", methods=["GET"])
def users_get():
    user_id = request.args.get("userId")
    if not user_id:
        return "No user id!", 400

    return f"GET UserId: {user_id}", 200

if __name__ == '__main__':
    app.run(debug=True)

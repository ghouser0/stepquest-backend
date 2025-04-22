from flask import Flask, request
from functools import wraps

# this is for authentication
# if someone tries to access smth they shouldnt, this will block that
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

@app.route('/test', methods=["GET", "POST"])
def test():
    match request.method:
        case "GET":
            return "Hello, this is GET"
        case "POST":
            return "Hello, POST"
        case _:
            return "WHAT?"


@app.route("/users/<userid>", methods=["POST"])
@deco()
def users_post(userid):
    user_id = userid #request.user_id
    if not user_id:
        return "No user id!", 400

    return f"POSTED UserId: {user_id}", 200

@app.route("/users/<userid>", methods=["GET"])
def users_get(userid):
    user_id = request.args.get("userId")
    if not user_id:
        return "No user id!", 400

    return f"GET UserId: {user_id}", 200 # maybe change to just returning userid


@app.route("/users/<userid>/steps", methods=["POST"])
@deco()
def steps_post(userid):
    # frontend needs to do smth with this to get apple health to update
    user_steps = request.user_steps
    # get user id of person trying to change and check
    if not user_steps:
        return "no user steps", 400
    
    return f"POST User steps = {user_steps}"

@app.route("/users/<userid>/steps", methods=["GET"])
def steps_get():
    user_steps = request.args.get("userSteps")
    if not user_steps:
        return "no user steps", 400
    
    return f"GET Usersteps = {user_steps}"



@app.route("/users/<userid>/achievements", methods=["GET"])
def achievements_get(userid):
    user_achievements = request.args.get("userAchievements")
    if not user_achievements:
        return "no achievements", 400
    return f"GET user ach = {user_achievements}"

@app.route("/users/<userid>/achievements", methods=["POST"])
@deco
def achievements_post(userid):
    user_achievements = request.user_achiements
    if not user_achievements:
        return "no user achievements", 400
    
    return f"POST User achievements = {user_achievements}"

if __name__ == '__main__':
    app.run(debug=True)

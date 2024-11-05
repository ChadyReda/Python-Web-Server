from functools import wraps
from flask import request, session, redirect

def auth_middlware(func):
    @wraps(func)
    def decorator_func(*args, **kwargs):
        print(f"handling request to {request.path} by auth_middlware")
        # check if the user exists or if it have a token we will verify that as well
        if "name" not in session or "id" not in session:
            return redirect("/login")
        return func(*args, **kwargs)
    return decorator_func
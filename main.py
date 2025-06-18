from fastapi import FastAPI, HTTPException
from models import User
from services import register_user, login_user
from schemas import LoginRequest

app = FastAPI()

# Post endpoint for user to register
@app.post("/register")
def register(user: User):
    success, msg = register_user(user)  # success: True or False followed by message; register_user is called to register the user
    if not success:
        raise HTTPException(status_code=400, detail=msg) #print error message if something(s) fails
    return {"message": "User registered successfully"} # message when registered successfully

# Post endpoint for user to login using email and password
@app.post("/login")
def login(login_req: LoginRequest):
    success, data = login_user(login_req.email, login_req.password) #similar to the one above, this time calling login_req to check if requirements are met
    if not success:
        raise HTTPException(status_code=401, detail=data) #error message
    return {"message": "Login successful", "user": data} #success message
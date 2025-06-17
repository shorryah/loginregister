from pydantic import BaseModel, EmailStr

#representation of the information of a single user registering
class User(BaseModel):
    name: str
    email: EmailStr #Emailstr used instead of str to validate if a valid email has been input
    phone: str
    password: str



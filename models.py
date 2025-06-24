from pydantic import BaseModel

#representation of the information of a single user registering
class User(BaseModel):
    name: str
    email: str
    phone: str
    password: str

#representation of the information of a single movie data
class Movie(BaseModel):
    title: str = " "
    description: str = " "

from database import collection 
from models import User
from passlib.context import CryptContext #used to hash and verify passwords; impt to protect a user's password
from schemas import format_user
import re  #regex module to check if password is appropriate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  #password hashing done using bycrpt

def hash_pw(pw):
    return pwd_context.hash(pw)  #returns hashed version of a password; if we output the password, a hashed version will be printed

def verify_pw(pw, hashed):
    return pwd_context.verify(pw, hashed)  #checks plain password with the hashed one

def is_valid_password(pw):
    regex = r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{9,}$"  #checks if password has at least 9 char, 1 Uppercase letter, 1 Special char and 1 num
    return re.match(regex, pw) 

def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 8  #checks if phone no. has 8 digits exact

def is_valid_name(name):
    return 2 < len(name) <= 70  # ensures that name is appropriate with at least 3-70 characters

def is_valid_email_domain(email):
    allowed_domains = ["gmail.com", "hotmail.com", "yahoo.com"] 
    domain = email.split("@")[1]
    return any(domain.endswith(d) for d in allowed_domains) or ".edu" in domain or ".org" in domain #checks for valid emails based on domain

#checks if registration is valid based on the above constraints
# if anything is invalid, the standard error message will be printed based on the error made
def register_user(user: User):
    if not is_valid_name(user.name):
        return False, "Name must be 70 characters or fewer"
    if not is_valid_phone(user.phone):
        return False, "Phone number must be exactly 8 digits"
    if not is_valid_password(user.password):
        return False, "Password must be 9+ chars with uppercase, number, and special character"
    if not is_valid_email_domain(user.email):
        return False, "Email must be from a valid domain (e.g., gmail.com, organisation)"

    if collection.find_one({"email": user.email}):  #to check if email already exists in database
        return False, "Email already registered"
    
    user.password = hash_pw(user.password)  #hashes password before saving
    collection.insert_one(user.model_dump())  #saves user to the database
    return True, "User saved" #success message

#checks whether login is valid using email and password
def login_user(email, password):
    user = collection.find_one({"email": email})  #find user through email
    if not user:
        return False, "Email not found"   #returns this message if email not found in database
    if not verify_pw(password, user["password"]):  
        return False, "Incorrect password"   #returns this message if password does not match the hashed one
    return True, "Login successful"   #returns this if both email and password is correct


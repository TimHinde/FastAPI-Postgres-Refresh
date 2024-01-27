import re
import yaml
from fastapi import APIRouter
from pydantic import BaseModel

from .. import database

router = APIRouter(prefix="/api", tags=["users"])


# User model - to be movced to models.py when needed
class User(BaseModel):
    name: str
    age: int
    email: str

db_config = yaml.safe_load(open("./env.yaml"))["DataBase"]

# Load database
db = database.Database(
    host=db_config["host"],
    port=db_config["port"],
    user=db_config["user"],
    password=db_config["password"],
    database="db_users"
)

@router.post("/users")
async def create_user(user: User):
    """
    Create a new user
    :param user: User object (dict of name, age, email)
    :return: message
    """
    print(user.name, user.age, user.email)
    # Connect to database and insert user
    User(name=user.name, age=user.age, email=user.email)

    # verify user data
    # verify name
    if not user.name:
        return {"message": "Name is required"}
    if len(user.name) < 3:
        return {"message": "Name must be at least 3 characters"}
    if len(user.name) > 50:
        return {"message": "Name must be less than 50 characters"}
    if not user.name.isalpha():
        return {"message": "Name must be alphabetic"}
    
    # verify age
    if not user.age:
        return {"message": "Age is required"}
    if type(user.age) != int:
        return {"message": "Age must be a whole number"}
 
    # verify email
    if not user.email:
        return {"message": "Email is required"}
    if not re.match(r"[^@]+@[^@]+\.[^@]+", user.email): # Upgrade for better regex later
        return {"message": "Invalid email"}
    if len(user.email) > 254:
        return {"message": "Email must be less than 254 characters"}
    
    # Check if user already exists
    user_check = await db.get_user_with_email(user.email)
    if user_check:
        data = {
            "name": user_check[0].get("name"),
            "age": user_check[0].get("age"),
            "email": user_check[0].get("email")
        }
        return {"message": f"User already exists: {data}"}
    
    #Logic to insert.
    await db.insert_user(user.name, user.age, user.email)
    
    # Check user inserted
    user= await db.get_user_with_email(user.email)
    if not user:
        return {"message": "User not insterted. Check logs for details."}
    
    # parse user data
    user_data = {
        "name": user[0].get("name"),
        "age": user[0].get("age"),
        "email": user[0].get("email")
    }
    # Return user data
    return {"message": f"User created successfully - {user_data.get('name')}"}

@router.get("/users/email")
async def get_user_with_email(email: str):
    # Logic to get a user
    user = await db.get_user_with_email(email)
    if not user:
        return {"message": "User not found"}
    # Return user data
    user_data = {
        "name": user.name,
        "age": user.age,
        "email": user.email
    }
    return {"message": f"User with ID {user.id} retrieved successfully - {user_data}"}

@router.get("/users/{user_id}")
async def get_user_with_id(user_id: int):
    # Logic to get a user
    user = db.get_user_with_id(user_id)
    if not user:
        return {"message": "User not found"}
    # Return user data
    user_data = {
        "name": user.name,
        "age": user.age,
        "email": user.email
    }
    return {"message": f"User with ID {user_id} retrieved successfully - {user_data}"}

@router.get("/users")
async def get_users():
    # Logic to get a user
    users = await db.get_all_users()
    if not users:
        return {"message": "Users not found"}
    # Return user data
    data = []
    for user in users:
        data.append({
            "name": user.get('name'),
            "age": user.get('age'),
            "email": user.get('email')
        })
    
    return {"message": "Users retrieved successfully", "data": data}

@router.put("/users/{user_id}")
async def update_user(user_id: int, user: User):
    # Logic to update a user
    # verify user data
    # verify id
    if not user_id:
        return {"message": "ID is required"}
    if type(user_id) != int:
        return {"message": "ID must be a whole number"}
    
    name = user.name
    age = user.age
    email = user.email
    

    print(name, age, email)
    # verify user data
    # verify name
    if name:
        if len(user.name) < 3:
            return {"message": "Name must be at least 3 characters"}
        if len(user.name) > 50:
            return {"message": "Name must be less than 50 characters"}
        if not user.name.isalpha():
            return {"message": "Name must be alphabetic"}
        
    
    # verify age
    if age:
        if type(user.age) != int:
            return {"message": "Age must be a whole number"}
 
    # verify email
    if email:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", user.email): # Upgrade for better regex later
            return {"message": "Invalid email"}
        if len(user.email) > 254:
            return {"message": "Email must be less than 254 characters"}
    
    # Check if user exists
    user_check = await db.get_user_with_id(user_id)
    if not user_check:
        return {"message": "User not found"}
    
    # convert to dict to handle None values
    user_data = user.dict()
    # Check if user data is empty
    if not user_data:
        return {"message": "No data"}


    
    #Logic to update.
    await db.update_user(user_id, name, age, email)
    
    # Return user data
    return {"message": f"User with ID {user_id} updated successfully"}


@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    # Logic to delete a user
    return {"message": f"User with ID {user_id} deleted successfully"}

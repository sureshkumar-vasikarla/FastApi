from fastapi import FastAPI, HTTPException
from supabase import create_client, Client

# Initialize FastAPI
app = FastAPI()

# Supabase credentials
SUPABASE_URL = "https://bxdvurymrpxjrhyzxiug.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ4ZHZ1cnltcnB4anJoeXp4aXVnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDIwMDc2NDksImV4cCI6MjA1NzU4MzY0OX0.UchDhnFlLifePTI6WhvP8maGrmMUf3hHSAThcVhi5JA"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Test endpoint
# @app.get("/")
# def read_root():
#     return {"message": supabase}


# @app.post("/todos/")
# def create_todo(task: str, completed: bool = False):
#     try:
#         data = supabase.table("todos").insert({"task": task, "completed": completed}).execute()
#         return data
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @app.get("/todos/")
# def get_todos():
#     try:
#         data = supabase.table("todos").select("*").execute()
#         return data
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @app.put("/todos/{todo_id}")
# def update_todo(todo_id: int, completed: bool):
#     try:
#         data = supabase.table("todos").update({"completed": completed}).eq("id", todo_id).execute()
#         return data
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @app.delete("/todos/{todo_id}")
# def delete_todo(todo_id: int):
#     try:
#         data = supabase.table("todos").delete().eq("id", todo_id).execute()
#         return {"message": "Todo deleted successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e)) 

#uvicorn main:app --reload

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client
from jose import JWTError, jwt
from pydantic import BaseModel
import pdb
import jwt as pyjwt
# Initialize FastAPI
app = FastAPI()

# Supabase credentials
SUPABASE_URL = "https://bxdvurymrpxjrhyzxiug.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ4ZHZ1cnltcnB4anJoeXp4aXVnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDIwMDc2NDksImV4cCI6MjA1NzU4MzY0OX0.UchDhnFlLifePTI6WhvP8maGrmMUf3hHSAThcVhi5JA"
JWT_Key="SBS179XQJ5zOc6JVRxbd8tQonUlD3ORUt0H+k0uyRHfqvI6lhgdFjqhn41SKI+tD2xLaMuhenKuLF1pnPDkeVg=="
# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Security setup
security = HTTPBearer()

# JWT verification
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    pdb.set_trace()
    token = credentials.credentials  #token
    payload = None
    try:
        #Verify the token using Supabase's public key
        
        print("Token:", token)
        token = token.replace("Bearer", "").strip()
        payload = jwt.decode(
            token,
            JWT_Key,  # Supabase's public key
            algorithms=["HS256"],
            options={"verify_aud": False}  # Supabase tokens don't have an audience
        )
        
        user_email = payload.get("email")
        if user_email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        return user_email
    except JWTError as e:
        print("JWT Error:", str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"+token,
        )

# # Model for creating a todo
# class TodoCreate(BaseModel):
#     task: str
#     completed: bool = False

# # Model for updating a todo
# class TodoUpdate(BaseModel):
#     task: str = None
#     completed: bool = None


# # Sign up endpoint
# @app.post("/signup/")
# def sign_up(email: str, password: str):
#     try:
#         user = supabase.auth.sign_up({"email": email, "password": password})
#         return {"message": "User created successfully", "user": user}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# # Login endpoint
# @app.post("/login/")
# def login(email: str, password: str):
#     try:
#         user = supabase.auth.sign_in_with_password({"email": email, "password": password})
#         return {"message": "Login successful", "token": user.session.access_token}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
# # Get all todos (protected)
# @app.get("/todos/")
# def get_todos(user_email: str = Depends(get_current_user)):
#     try:
#         data = supabase.table("todos").select("*").eq("user_email", user_email).execute()
#         return data
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# # Create a new todo (protected)
# @app.post("/todos/")
# def create_todo(todo: TodoCreate, user_email: str = Depends(get_current_user)):
#     pdb.set_trace()
#     try:
#         data = supabase.table("todos").insert({"task": todo.task, "completed": todo.completed, "user_email": user_email}).execute()
#         return data
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# # Update a todo (protected)
# @app.put("/todos/{todo_id}")
# def update_todo(todo_id: int, todo: TodoUpdate, user_email: str = Depends(get_current_user)):
#     try:
#         update_data = {}
#         if todo.task is not None:
#             update_data["task"] = todo.task
#         if todo.completed is not None:
#             update_data["completed"] = todo.completed

#         data = supabase.table("todos").update(update_data).eq("id", todo_id).eq("user_email", user_email).execute()
#         return data
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# # Delete a todo (protected)
# @app.delete("/todos/{todo_id}")
# def delete_todo(todo_id: int, user_email: str = Depends(get_current_user)):
#     try:
#         data = supabase.table("todos").delete().eq("id", todo_id).eq("user_email", user_email).execute()
#         return {"message": "Todo deleted successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

#==========================================================================================================#

# Profile model
class ProfileCreate(BaseModel):
    name: str
    email: str
    avatar_url: str = None
    phone: str = None
@app.post("/profiles/")

def create_profile(profile: ProfileCreate, user_id: str = Depends(get_current_user)):
    try:
        # Check if the profile already exists
        existing_profile = supabase.table("profiles").select("*").eq("id", user_id).execute()
        if existing_profile.data:
            raise HTTPException(status_code=400, detail="Profile already exists")

        # Insert the profile
        data = supabase.table("profiles").insert({
            "id": user_id,
            "name": profile.name,
            "email": profile.email,
            "avatar_url": profile.avatar_url,
            "phone": profile.phone
        }).execute()
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))    
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Response, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client
from jose import JWTError, jwt
from pydantic import BaseModel
import pdb
import uuid

# Initialize FastAPI
app = FastAPI()
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from Next.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Supabase credentials

SUPABASE_URL = "https://bxdvurymrpxjrhyzxiug.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ4ZHZ1cnltcnB4anJoeXp4aXVnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MjAwNzY0OSwiZXhwIjoyMDU3NTgzNjQ5fQ.iA-SJo_RCN1EdIaCM91yo21pJIRFVOHVWWpknK5895I"
JWT_Key="SBS179XQJ5zOc6JVRxbd8tQonUlD3ORUt0H+k0uyRHfqvI6lhgdFjqhn41SKI+tD2xLaMuhenKuLF1pnPDkeVg=="
# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Security setup
security = HTTPBearer()

# JWT verification
async def get_current_user(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    pdb.set_trace()

     # Try to get the token from the cookie first
    token = request.cookies.get("auth_token")
    # If the cookie is not present, try to get the token from the Authorization header
    if not token and credentials:
        token = credentials.credentials
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
        
        user_id = payload["user_metadata"].get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        return user_id
    except JWTError as e:
        print("JWT Error:", str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"+token,
        )



# Signup model
class SignupRequest(BaseModel):
    email: str
    password: str
    name: str
    avatar_url: str = None
    phone: str = None

# Signup endpoint
@app.post("/signup/")
def signup(user: SignupRequest):
    pdb.set_trace()
    try:
        # Generate a unique email address
        unique_email = f"{uuid.uuid4()}@example.com"
        # Step 1: Sign up the user using Supabase Auth
        auth_response = supabase.auth.sign_up({
            "email": unique_email,
            "password": user.password
        })

        # Check if signup was successful
        if not auth_response.user:
            raise HTTPException(status_code=400, detail="Signup failed")

        # Step 2: Create a profile in the profiles table
        profile_data = {
            "id": auth_response.user.id,  # Use the user ID from Supabase Auth
            "name": user.name,
            "email": unique_email,
            "avatar_url": user.avatar_url,
            "phone": user.phone
        }

        print("Profile data:", profile_data)
        supabase.table("profiles").insert(profile_data).execute()

        return {"message": "Signup successful", "user": auth_response.user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
# Login model
class LoginRequest(BaseModel):
    email: str
    password: str

# Login endpoint
@app.post("/login/")
def login(user: LoginRequest,response: Response):
    try:
        pdb.set_trace()
        # Log in the user using Supabase Auth
        auth_response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })

        # Check if login was successful
        if not auth_response.user:
            raise HTTPException(status_code=400, detail="Login failed")
        #auth_response.session.access_token,
        # Set an HTTP-only cookie with the token
        response.set_cookie(
            key="auth_token",
            value=auth_response.session.access_token,
            httponly=True,  # Prevent JavaScript access
            secure=False,    # Set to False for HTTP (localhost)
            samesite="None",  # Prevent CSRF attacks
            max_age=86400,   # Cookie expiration time (e.g., 1 day)
            domain="localhost",  # Set the domain (e.g., localhost)
            path="/",            # Set the path (e.g., root path)
    )
        data = supabase.table("profiles").select("*").eq("id",  auth_response.user.id).execute()
        # Return the JWT token
        return {"message": "Login successful","data":data.data[0], "token": auth_response.session.access_token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



# Profile model
class Profile(BaseModel):
    name: str
    email: str
    avatar_url: str
    phone: str

# Get user profile
@app.get("/profiles/me")
def get_profile(user_id: str = Depends(get_current_user)):
    try:
        data = supabase.table("profiles").select("*").eq("id", user_id).execute()
        if not data.data:
            raise HTTPException(status_code=404, detail="Profile not found")
        return data.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/profiles/me")
def update_profile(profile: Profile, user_id: str = Depends(get_current_user)):
    try:
        pdb.set_trace()
        data = supabase.table("profiles").update(profile.dict()).eq("id", user_id).execute()
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class ContactCreate(BaseModel):
    contact_id: str  # UUID of the contact

# Add a contact
@app.post("/contacts/")
def add_contact(contact: ContactCreate, user_id: str = Depends(get_current_user)):
    try:
        pdb.set_trace()
        data = supabase.table("contacts").insert({
            "user_id": user_id,
            "contact_id": contact.contact_id
        }).execute()
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/contacts/")
def get_contacts(user_id: str = Depends(get_current_user)):
    try:
        data = supabase.table("contacts").select("*").eq("user_id", user_id).execute()
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: str, user_id: str = Depends(get_current_user)):
    try:
        data = supabase.table("contacts").delete().eq("user_id", user_id).eq("contact_id", contact_id).execute()
        return {"message": "Contact deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class GroupCreate(BaseModel):
    name: str
    avatar_url: str

# Create a group
@app.post("/groups/")
def create_group(group: GroupCreate, user_id: str = Depends(get_current_user)):
    try:
        data = supabase.table("groups").insert({
            "name": group.name,
            "avatar_url": group.avatar_url,
            "created_by": user_id
        }).execute()
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/groups/")
def get_groups(user_id: str = Depends(get_current_user)):
    try:
        data = supabase.table("groups").select("*").eq("created_by", user_id).execute()
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class GroupMemberCreate(BaseModel):
    group_id: str
    user_id: str

# Add a group member
@app.post("/group-members/")
def add_group_member(member: GroupMemberCreate, user_id: str = Depends(get_current_user)):
    try:
        # Check if the user is the group creator
        group = supabase.table("groups").select("*").eq("id", member.group_id).eq("created_by", user_id).execute()
        if not group.data:
            raise HTTPException(status_code=403, detail="You are not the group creator")

        data = supabase.table("group_members").insert({
            "group_id": member.group_id,
            "user_id": member.user_id
        }).execute()
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/group-members/{group_id}")
def get_group_members(group_id: str, user_id: str = Depends(get_current_user)):
    try:
        # Check if the user is a member of the group
        member = supabase.table("group_members").select("*").eq("group_id", group_id).eq("user_id", user_id).execute()
        if not member.data:
            raise HTTPException(status_code=403, detail="You are not a member of this group")

        data = supabase.table("group_members").select("*").eq("group_id", group_id).execute()
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class MessageCreate(BaseModel):
    receiver_id: str = None  # For direct messages
    group_id: str = None  # For group messages
    content: str

# Send a message
@app.post("/messages/")
def send_message(message: MessageCreate, user_id: str = Depends(get_current_user)):
    try:
        if not message.receiver_id and not message.group_id:
            raise HTTPException(status_code=400, detail="Either receiver_id or group_id is required")

        data = supabase.table("messages").insert({
            "sender_id": user_id,
            "receiver_id": message.receiver_id,
            "group_id": message.group_id,
            "content": message.content
        }).execute()
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/messages/")
def get_messages(user_id: str = Depends(get_current_user)):
    try:
        data = supabase.table("messages").select("*").or_(
            f"sender_id.eq.{user_id},receiver_id.eq.{user_id},group_id.in.(SELECT group_id FROM group_members WHERE user_id.eq.{user_id})"
        ).execute()
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class AttachmentCreate(BaseModel):
    message_id: str
    file_name: str
    file_type: str
    file_size: int
    file_url: str

# Add an attachment
@app.post("/attachments/")
def add_attachment(attachment: AttachmentCreate, user_id: str = Depends(get_current_user)):
    try:
        # Check if the user is the sender of the message
        message = supabase.table("messages").select("*").eq("id", attachment.message_id).eq("sender_id", user_id).execute()
        if not message.data:
            raise HTTPException(status_code=403, detail="You are not the sender of this message")

        data = supabase.table("attachments").insert(attachment.dict()).execute()
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
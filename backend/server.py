from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from bson import ObjectId
import re

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Security
SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-change-in-production-12345678")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Create the main app
app = FastAPI(title="B2B Mobile API")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise credentials_exception
    
    return user

def require_role(allowed_roles: List[str]):
    async def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return role_checker

# Models
class UserCreate(BaseModel):
    email: EmailStr
    mobile: str
    password: str
    name: str
    role: str  # Admin, Sales, Buyer
    company_name: Optional[str] = None

class UserLogin(BaseModel):
    login: str  # email or mobile
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

class UserResponse(BaseModel):
    id: str
    email: str
    mobile: str
    name: str
    role: str
    company_id: Optional[str] = None
    company_name: Optional[str] = None
    created_at: datetime
    is_active: bool

class DashboardStats(BaseModel):
    total_orders: int = 0
    pending_orders: int = 0
    completed_orders: int = 0
    total_products: int = 0
    low_stock_products: int = 0
    total_vendors: int = 0
    pending_payments: int = 0
    total_revenue: float = 0.0

# Auth Routes
@api_router.post("/auth/register", response_model=Token)
async def register(user_data: UserCreate):
    # Validate role
    if user_data.role not in ["Admin", "Sales", "Buyer"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    # Check if email exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if mobile exists
    existing_mobile = await db.users.find_one({"mobile": user_data.mobile})
    if existing_mobile:
        raise HTTPException(status_code=400, detail="Mobile number already registered")
    
    # Validate mobile format (basic validation)
    if not re.match(r'^[+]?[0-9]{10,15}$', user_data.mobile.replace(" ", "")):
        raise HTTPException(status_code=400, detail="Invalid mobile number format")
    
    # Create or get company
    company_id = None
    company_name = user_data.company_name or "Default Company"
    
    company = await db.companies.find_one({"name": company_name})
    if not company:
        company_doc = {
            "name": company_name,
            "created_at": datetime.utcnow()
        }
        result = await db.companies.insert_one(company_doc)
        company_id = str(result.inserted_id)
    else:
        company_id = str(company["_id"])
    
    # Create user
    user_doc = {
        "email": user_data.email,
        "mobile": user_data.mobile,
        "password_hash": get_password_hash(user_data.password),
        "name": user_data.name,
        "role": user_data.role,
        "company_id": company_id,
        "company_name": company_name,
        "created_at": datetime.utcnow(),
        "is_active": True
    }
    
    result = await db.users.insert_one(user_doc)
    user_id = str(result.inserted_id)
    
    # Create token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_id}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user_id,
            "email": user_data.email,
            "mobile": user_data.mobile,
            "name": user_data.name,
            "role": user_data.role,
            "company_id": company_id,
            "company_name": company_name
        }
    }

@api_router.post("/auth/login", response_model=Token)
async def login(credentials: UserLogin):
    # Try to find user by email or mobile
    user = await db.users.find_one({
        "$or": [
            {"email": credentials.login},
            {"mobile": credentials.login}
        ]
    })
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/mobile or password"
        )
    
    if not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/mobile or password"
        )
    
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    # Create token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user["_id"])}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user["_id"]),
            "email": user["email"],
            "mobile": user["mobile"],
            "name": user["name"],
            "role": user["role"],
            "company_id": user.get("company_id"),
            "company_name": user.get("company_name")
        }
    }

@api_router.get("/auth/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    return {
        "id": str(current_user["_id"]),
        "email": current_user["email"],
        "mobile": current_user["mobile"],
        "name": current_user["name"],
        "role": current_user["role"],
        "company_id": current_user.get("company_id"),
        "company_name": current_user.get("company_name"),
        "created_at": current_user["created_at"],
        "is_active": current_user.get("is_active", True)
    }

# Dashboard Routes
@api_router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(current_user: dict = Depends(get_current_user)):
    stats = DashboardStats()
    
    # Get company-specific data
    company_id = current_user.get("company_id")
    
    # Count orders (placeholder - will be implemented in Phase 3)
    stats.total_orders = 0
    stats.pending_orders = 0
    stats.completed_orders = 0
    
    # Count products (placeholder - will be implemented in Phase 2)
    stats.total_products = 0
    stats.low_stock_products = 0
    
    # Count vendors (placeholder - will be implemented in Phase 4)
    stats.total_vendors = 0
    
    # Payment stats (placeholder - will be implemented in Phase 5)
    stats.pending_payments = 0
    stats.total_revenue = 0.0
    
    return stats

# User Management Routes (Admin only)
@api_router.get("/users", response_model=List[UserResponse])
async def get_users(current_user: dict = Depends(require_role(["Admin"]))):
    company_id = current_user.get("company_id")
    users = await db.users.find({"company_id": company_id}).to_list(1000)
    
    return [
        {
            "id": str(user["_id"]),
            "email": user["email"],
            "mobile": user["mobile"],
            "name": user["name"],
            "role": user["role"],
            "company_id": user.get("company_id"),
            "company_name": user.get("company_name"),
            "created_at": user["created_at"],
            "is_active": user.get("is_active", True)
        }
        for user in users
    ]

# Health check
@api_router.get("/")
async def root():
    return {"message": "B2B Mobile API", "status": "running"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

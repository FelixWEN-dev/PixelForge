"""
用户认证路由
"""

from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session

from models.database_models import User, SessionLocal, get_db

router = APIRouter(prefix="/api/v1/auth", tags=["用户认证"])


# ========== 请求/响应模型 ==========

class RegisterRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str


class AuthResponse(BaseModel):
    success: bool
    message: str = None
    data: dict = None


# ========== 辅助函数 ==========

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, username: str, password: str):
    db_user = User(username=username, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ========== API 路由 ==========

@router.post("/register", response_model=AuthResponse)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    用户注册
    """
    # 检查用户名是否已存在
    existing_user = get_user_by_username(db, request.username)
    if existing_user:
        return AuthResponse(success=False, message="用户名已存在")
    
    # 创建新用户
    user = create_user(db, request.username, request.password)
    
    # 生成简单 token (实际项目中应使用 JWT)
    token = f"user_{user.id}_{user.username}"
    
    return AuthResponse(
        success=True,
        message="注册成功",
        data={
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username
            }
        }
    )


@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    用户登录
    """
    user = get_user_by_username(db, request.username)
    if not user:
        return AuthResponse(success=False, message="用户名或密码错误")
    
    # 验证密码 (明文比较)
    if user.password != request.password:
        return AuthResponse(success=False, message="用户名或密码错误")
    
    # 生成 token
    token = f"user_{user.id}_{user.username}"
    
    return AuthResponse(
        success=True,
        message="登录成功",
        data={
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username
            }
        }
    )


@router.get("/me", response_model=AuthResponse)
async def get_me(authorization: str = Header(None), db: Session = Depends(get_db)):
    """
    获取当前用户信息
    """
    if not authorization or not authorization.startswith("Bearer "):
        return AuthResponse(success=False, message="未登录")
    
    token = authorization.replace("Bearer ", "")
    
    # 解析 token (简化版)
    try:
        parts = token.split("_")
        if len(parts) >= 2:
            user_id = int(parts[1])
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                return AuthResponse(
                    success=True,
                    data={
                        "user": {
                            "id": user.id,
                            "username": user.username
                        }
                    }
                )
    except:
        pass
    
    return AuthResponse(success=False, message="登录已过期")

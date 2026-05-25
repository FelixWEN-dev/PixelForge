"""
SQLAlchemy 数据库模型
"""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# 数据库配置 (MySQL)
DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/pixelforge"


engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    pool_pre_ping=True,  # 自动检测断开的连接
    pool_recycle=3600,   # 1小时后回收连接
    pool_size=10,        # 连接池大小
    max_overflow=20      # 超出连接池大小时的最大连接数
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # 关联历史记录
    histories = relationship("GenerationHistory", back_populates="user", cascade="all, delete-orphan")


class GenerationHistory(Base):
    """生成历史记录表"""
    __tablename__ = "generation_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, comment="用户ID")
    task_id = Column(String(50), unique=True, nullable=False, index=True)
    asset_type = Column(String(20), nullable=False)
    description = Column(Text, nullable=False)
    style = Column(String(50), default="像素风")
    size = Column(String(20), default="1024*1024")
    n = Column(Integer, default=1)
    watermark = Column(Integer, default=0)  # 0=false, 1=true
    model = Column(String(100))
    prompt = Column(Text)
    local_paths = Column(JSON, default=list)  # 本地路径数组
    status = Column(String(20), default="pending")  # pending/processing/completed/failed
    created_at = Column(DateTime, default=datetime.now)

    # 关联用户
    user = relationship("User", back_populates="histories")


def create_tables():
    """创建所有表"""
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表创建成功!")


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    create_tables()

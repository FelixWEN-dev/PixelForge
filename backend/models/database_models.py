"""
SQLAlchemy 数据库模型
"""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库配置 (MySQL)
DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/pixelforge"

# SQLite 配置（备用）
# DATABASE_URL = "sqlite:///./pixelforge.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class GenerationHistory(Base):
    """生成历史记录表"""
    __tablename__ = "generation_history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String(50), unique=True, nullable=False, index=True)
    asset_type = Column(String(20), nullable=False)
    description = Column(Text, nullable=False)
    style = Column(String(50), default="像素风")
    size = Column(String(20), default="1024*1024")
    n = Column(Integer, default=1)
    watermark = Column(Integer, default=0)  # 0=false, 1=true
    model = Column(String(50))
    prompt = Column(Text)
    local_paths = Column(JSON, default=list)  # 本地路径数组
    status = Column(String(20), default="pending")  # pending/processing/completed/failed
    created_at = Column(DateTime, default=datetime.now)


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

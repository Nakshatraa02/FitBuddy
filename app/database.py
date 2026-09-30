from sqlalchemy import Column, Integer, String, Float, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "sqlite:///./fitbuddy.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(String, index=True)
    username = Column(String)

    age = Column(Integer)
    weight = Column(Float)
    goal = Column(String)
    intensity = Column(String)

    original_workout_plan = Column(Text)
    updated_workout_plan = Column(Text, nullable=True)

    nutrition_tip = Column(Text)
    feedback = Column(Text, nullable=True)


Base.metadata.create_all(bind=engine)
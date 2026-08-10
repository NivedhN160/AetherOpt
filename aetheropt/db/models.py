import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, Float, ForeignKey
from sqlalchemy.orm import relationship
from aetheropt.db.base import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    problem_type = Column(String, index=True)
    status = Column(String, index=True)  # pending, running, completed, failed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    config = Column(JSON, default=dict)
    error_message = Column(String, nullable=True)
    
    results = relationship("Result", back_populates="job", cascade="all, delete-orphan")

class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, ForeignKey("jobs.id"))
    solver_name = Column(String, index=True)
    best_solution = Column(JSON)
    objective_value = Column(Float)
    runtime_seconds = Column(Float)
    metadata = Column(JSON, default=dict)

    job = relationship("Job", back_populates="results")

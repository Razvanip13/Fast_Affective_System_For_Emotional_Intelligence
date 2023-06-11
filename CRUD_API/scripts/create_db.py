from sqlmodel import SQLModel
from repository.database import engine
import domain.models

print("CREATING DATABASE.....")

SQLModel.metadata.create_all(engine)
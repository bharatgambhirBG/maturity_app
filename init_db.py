from data.db import Base, engine
import data.models   # ensures all models are registered

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done.")
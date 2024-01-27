from fastapi import FastAPI
from app.routers import user
from app.database import Database
import yaml

# Create app

app = FastAPI()

# Set user router
app.include_router(user.router)

# Load configs
configs = yaml.safe_load(open("env.yaml"))
db_config = configs["DataBase"]

# Create database
#
async def __init__ ():
    print(f"Running {configs['App']}")
    db = Database(
        host=db_config["host"],
        port=db_config["port"],
        user=db_config["user"],
        password=db_config["password"],
        database="db_users"
    )
    
    await db.create_table()
    # Check for table
    await db.check_table()

    # await db.disconnect() \\ This is not needed as the connection is closed automatically.

# Run on startup


@app.on_event("startup")
async def startup():
    await __init__()

@app.on_event("shutdown")
async def shutdown():
    print("Goobye, and thanks for all the fish.")
# Run app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

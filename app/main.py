from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello, world"}

@app.get("/hello")
def hello_name(name: str = "World"):
    return {"message": f"Hello, {name}"}
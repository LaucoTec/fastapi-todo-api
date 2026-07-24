from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Stage 0: Hello Server"}

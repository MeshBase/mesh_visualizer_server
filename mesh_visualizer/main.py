from fastapi import FastAPI


app = FastAPI(
    title="Mesh Visualizer API",
    description="API for visualizing 3D meshes",
    version="1.0.0",
    openapi_tags=[
        {"name": "Mesh", "description": "Operations related to 3D mesh visualization"}
    ],
)


@app.get("/", tags=["Mesh"])
async def read_root():
    return {"message": "Welcome to the Mesh Visualizer API!"}


@app.get("/health", tags=["Mesh"])
async def health_check():
    return {"status": "healthy"}

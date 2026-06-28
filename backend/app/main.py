from fastapi import FastAPI

app = FastAPI(
    title="OpsMind API",
    version="0.1.0",
    description="AI Operations Platform powered by GraphRAG",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}
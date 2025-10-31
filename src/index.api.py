from fastapi import FastAPI
app = FastAPI(title="SimStack API")

@app.get("/")
def root():
    return {"status": "ok"}

# Ejecuta con:  uvicorn "src.index.api:app" --reload --port 8000  (desde la carpeta raíz)

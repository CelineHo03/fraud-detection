from fastapi import FastAPI 
from app.config import settings

app = FastAPI(
    title = 'Fraud Detection System',
    description = 'Vietnamese Banking Fraud Detection API',
    version = '0.1.0'
)

@app.get('/')
async def root():
    return {
        "status": "online",
        "service": "Fraud Detection API",
        "version": "0.1.0"
    }

@app.get('/health')
async def health():
    return {'status': 'healthy'}

if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(app, host = "0.0.0.0", port = 8000)
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from sqlalchemy.orm import Session
from typing import List
import json

from . import models, schemas, database

from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Honeypot Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# API endpoint to view logs securely (basic implementation, should add auth)
@app.get("/api/logs", response_model=List[schemas.AttackLogResponse])
def get_logs(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    logs = db.query(models.AttackLog).order_by(models.AttackLog.timestamp.desc()).offset(skip).limit(limit).all()
    return logs

# Catch-all route for any HTTP method and any path
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def catch_all(request: Request, path: str, db: Session = Depends(database.get_db)):
    # Extract request information
    client_ip = request.client.host if request.client else "unknown"
    method = request.method
    full_path = request.url.path
    headers = dict(request.headers)
    query_params = dict(request.query_params)
    
    # Read body if possible
    body = ""
    try:
        body_bytes = await request.body()
        body = body_bytes.decode("utf-8")
    except Exception:
        body = "<binary or non-utf8 data>"

    user_agent = request.headers.get("user-agent", "unknown")

    # Create log entry
    log_entry = models.AttackLog(
        ip_address=client_ip,
        method=method,
        path=full_path,
        headers=json.dumps(headers),
        query_params=json.dumps(query_params),
        body=body,
        user_agent=user_agent
    )

    # Save to database
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)

    # Return a generic response to simulate a standard web server
    # Many attackers look for specific vulnerable paths like wp-admin, phpmyadmin, etc.
    # We just return a standard 404 to look like a normal web server
    return JSONResponse(status_code=404, content={"error": "Not Found"})

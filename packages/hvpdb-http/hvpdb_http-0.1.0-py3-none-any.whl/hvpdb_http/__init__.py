import typer
import uvicorn
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
try:
    from hvpdb.utils import connect_db
    from hvpdb.core import HVPDB
except ImportError:
    HVPDB = None
    connect_db = None
app = typer.Typer(help='HVPDB HTTP Server Plugin')
api = FastAPI(title='HVPDB API', description='HTTP Interface for HVPDB')
db_instance = None

class QueryRequest(BaseModel):
    query: Dict[str, Any]
    limit: int = 10

class InsertRequest(BaseModel):
    data: Dict[str, Any]

@api.get('/')
def read_root():
    return {'status': 'ok', 'service': 'HVPDB API'}

@api.get('/groups')
def list_groups():
    if not db_instance:
        raise HTTPException(500, 'DB not connected')
    return {'groups': db_instance.get_all_groups()}

@api.post('/{group}/insert')
def insert_doc(group: str, req: InsertRequest):
    if not db_instance:
        raise HTTPException(500, 'DB not connected')
    res = db_instance.group(group).insert(req.data)
    db_instance.commit()
    return res

@api.post('/{group}/find')
def find_docs(group: str, req: QueryRequest):
    if not db_instance:
        raise HTTPException(500, 'DB not connected')
    docs = db_instance.group(group).find(req.query)
    return docs[:req.limit]

@app.command(name='start')
def start_server(target: str=typer.Argument(..., help='Database Path'), port: int=typer.Argument(8000, help='Port'), host: str=typer.Argument('127.0.0.1', help='Host'), password: Optional[str]=typer.Argument(None, help='DB Password')):
    global db_instance
    if not connect_db:
        print('Error: hvpdb core not found.')
        return
    try:
        db_instance = connect_db(target, password)
        print(f'Connected to {target}')
        uvicorn.run(api, host=host, port=port)
    except Exception as e:
        print(f'Error: {e}')

@app.command(name='ping')
def remote_ping(url: str=typer.Argument(..., help='Server URL (e.g. http://localhost:8000)')):
    try:
        import requests
    except ImportError:
        print("Error: 'requests' library required. pip install requests")
        return
    try:
        resp = requests.get(url + '/')
        if resp.status_code == 200:
            print(f'✅ Pong! Server is up. {resp.json()}')
        else:
            print(f'❌ Server returned {resp.status_code}')
    except Exception as e:
        print(f'❌ Connection failed: {e}')

@app.command(name='remote-stats')
def remote_stats(url: str=typer.Argument(..., help='Server URL')):
    try:
        import requests
    except ImportError:
        print("Error: 'requests' library required.")
        return
    try:
        resp = requests.get(url + '/groups')
        if resp.status_code == 200:
            print(f"Groups: {resp.json()['groups']}")
        else:
            print(f'Error: {resp.status_code}')
    except Exception as e:
        print(f'Connection failed: {e}')
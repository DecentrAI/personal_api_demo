import uuid

from fastapi import FastAPI, Request, HTTPException
from starlette.responses import JSONResponse

from time import time

from dummy_epoch_manager import DummyEpochManager 

__VER__ = '0.1.3'

WORKER_ID = "0xai_" + str(uuid.uuid4())[:5]

INFO = """
## Simple demo/mockup FastAPI application 
  - designed to be run in a Docker container and exposed to the internet using ngrok 
  - for development and testing purposes of the Epoch Oracle
  - can be used for smart contract testing and development
"""

eng = DummyEpochManager()

app = FastAPI(
    title="Simple Epoch Oracle API",
    summary="Simple Epoch Oracle API using FastAPI, uvicorn, Docker and ngrok",
    description=INFO,
    version=__VER__,
    # terms_of_service="http://example.com/terms/",
    # contact={
    #     "name": "API Support",
    #     "url": "http://www.example.com/support",
    #     "email": "support@example.com",
    # },
    # license_info={
    #     "name": "Apache 2.0",
    #     "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    # },
)

# Simple in-memory rate limiter
REQUEST_LIMIT = 5 # demo limit
time_window = 10  # demo window in seconds
request_counts = {}


@app.middleware("http")
async def naive_rate_limitter(request: Request, call_next):
  client_ip = request.client.host
  current_time = time()
  
  # Implementing a very basic rate limiting
  if client_ip not in request_counts:
    request_counts[client_ip] = {"count": 1, "time": current_time}
  else:
    if current_time - request_counts[client_ip]["time"] <= time_window:
      if request_counts[client_ip]["count"] > REQUEST_LIMIT:
        return JSONResponse(
          content={"message": "Rate limit exceeded"},
          status_code=429
        )
      # endif request count outside limit
      request_counts[client_ip]["count"] += 1
    else:
      request_counts[client_ip] = {"count": 1, "time": current_time}
    # endif within window or not
  return await call_next(request)


def get_response(dct_data: dict):
  dct_data['worker_id'] = WORKER_ID
  return dct_data

@app.get("/")
async def root():
  return get_response({
    "msg": f"Epoch API Demo. Please use /docs for extended documentation.", 
    "version": __VER__
  })


@app.get("/node_epoch")
async def node_status(node_addr: str, epoch: int):
  result = eng.get_node_epoch(node_addr, epoch)
  current_epoch = eng.get_current_epoch()
  if result is None:
    raise HTTPException(status_code=404, detail="Node not found")
  return get_response({
    "node": node_addr, "epoch": epoch, "value": result, "current_epoch": current_epoch
  })


@app.get("/node_epochs")
async def node_status(node_addr: str):
  current_epoch = eng.get_current_epoch()
  result = eng.get_node_epochs(node_addr)
  if result is None:
    raise HTTPException(status_code=404, detail="Node not found")
  return get_response({
    "node": node_addr, "epochs": result, "current_epoch": current_epoch
  })


@app.get("/nodes_list")
async def nodes_list():
  nodes = eng.get_nodes_list()
  current_epoch = eng.get_current_epoch()
  return get_response({
    "nodes": nodes, "current_epoch": current_epoch
  })


@app.get("/node_last_epoch")
async def node_last_epoch(node_addr: str):
  current_epoch = eng.get_current_epoch()
  result = eng.get_node_last_epoch(node_addr)
  if result is None:
    raise HTTPException(status_code=404, detail="Node not found")
  return get_response({
    "node": node_addr, 
    "last_epoch": result, 
    "last_epoch_prc" : round(result / 255, 4),
    "current_epoch": current_epoch
  })


@app.get("/init_node")
async def init_node(node_addr: str):
  """This NOT a valid API in the actual system. This is a helper function for testing."""
  addr, epochs = eng.init_node(node_addr)
  return get_response({
    "node": addr, "status": "initialized", "epochs" : epochs
  })

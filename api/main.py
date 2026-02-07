from fastapi import FastAPI, Request
from vercel.functions import ip_address, geolocation
 
app = FastAPI()
 
@app.get("/api/status")
async def get_test_status(request: Request):
    return {"status": "success", "message": "Hello, World!"}


@app.get("/api/geo")
async def geo_info(request: Request):
    info = geolocation(request)
    return info


@app.get("/api/ip")
async def get_ip_address(request: Request):
    ip = ip_address(request)  # you can also pass request.headers
    return {"ip": ip}
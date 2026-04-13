from fastapi import FastAPI

app = FastAPI(title="ICID Reporting API", version="1.0.0")


def include_routers(app: FastAPI):
    from api.v1.users import router as users_router
    from api.v1.projects import router as projects_router

    app.include_router(users_router)
    app.include_router(projects_router)


include_routers(app)


@app.get("/status")
def get_status():
    return {"status": "ok", "message": "ICID API is running"}

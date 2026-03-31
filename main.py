from fastapi import FastAPI

app = FastAPI()

# move imports *AFTER* app creation and inside a function
def include_routers(app):
    from api.v1.users import router as users_router
    # from api.v1.clients import router as clients_router
    # from api.v1.projects import router as projects_router
    # from api.v1.project_users import router as project_users_router
    # from api.v1.project_clients import router as project_clients_router
    # from api.v1.reports import router as reports_router
    # from api.v1.form_templates import router as form_templates_router
    # from api.v1.completed_forms import router as completed_forms_router

    app.include_router(users_router)
    # app.include_router(clients_router)
    # app.include_router(projects_router)
    # app.include_router(project_users_router)
    # app.include_router(project_clients_router)
    # app.include_router(reports_router)
    # app.include_router(form_templates_router)
    # app.include_router(completed_forms_router)


include_routers(app)

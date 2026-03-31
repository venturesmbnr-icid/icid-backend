# schema.sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

------------------------------------------------------------
-- CLIENT
------------------------------------------------------------
CREATE TABLE clients (
    client_id       TEXT PRIMARY KEY,          
    client_username TEXT NOT NULL,
    client_name     TEXT NOT NULL,
    client_email    TEXT,
    client_phone    TEXT,
    client_role     TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_clients_client_id ON clients(client_id);
CREATE INDEX idx_clients_client_username ON clients(client_username);

------------------------------------------------------------
-- USER
------------------------------------------------------------
CREATE TABLE users (
    uuid            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email           TEXT NOT NULL,
    first_name      TEXT,
    last_name       TEXT,
    phone_number    TEXT,
    client_id       TEXT NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT fk_users_client
        FOREIGN KEY (client_id) REFERENCES clients(client_id)
);

CREATE INDEX idx_users_uuid ON users(uuid);
CREATE INDEX idx_users_email ON users(email);

------------------------------------------------------------
-- PROJECT
------------------------------------------------------------
CREATE TABLE projects (
    project_id          TEXT PRIMARY KEY,
    project_name        TEXT NOT NULL,
    project_description TEXT,
    registration_code   TEXT,
    borough             TEXT,
    status              TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_projects_project_id ON projects(project_id);

------------------------------------------------------------
-- PROJECT_USER (assignment table)
------------------------------------------------------------
CREATE TABLE project_users (
    project_id   TEXT NOT NULL,
    user_uuid    UUID NOT NULL,
    user_role    TEXT,
    assigned_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (project_id, user_uuid),
    CONSTRAINT fk_project_users_project
        FOREIGN KEY (project_id) REFERENCES projects(project_id),
    CONSTRAINT fk_project_users_user
        FOREIGN KEY (user_uuid) REFERENCES users(uuid)
);

CREATE INDEX idx_project_users_project ON project_users(project_id);
CREATE INDEX idx_project_users_user_uuid ON project_users(user_uuid);

------------------------------------------------------------
-- PROJECT_CLIENT (extra clients on project)
------------------------------------------------------------
CREATE TABLE project_clients (
    project_id   TEXT NOT NULL,
    client_id    TEXT NOT NULL,
    client_role  TEXT,
    PRIMARY KEY (project_id, client_id),
    CONSTRAINT fk_project_clients_project
        FOREIGN KEY (project_id) REFERENCES projects(project_id),
    CONSTRAINT fk_project_clients_client
        FOREIGN KEY (client_id) REFERENCES clients(client_id)
);

CREATE INDEX idx_project_clients_project ON project_clients(project_id);
CREATE INDEX idx_project_clients_client ON project_clients(client_id);

------------------------------------------------------------
-- REPORT
------------------------------------------------------------
CREATE TABLE reports (
    report_id          TEXT PRIMARY KEY,
    reporter_uuid      UUID NOT NULL,
    project_id         TEXT NOT NULL,
    report_date        DATE,
    created_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT fk_reports_project
        FOREIGN KEY (project_id) REFERENCES projects(project_id),
    CONSTRAINT fk_reports_reporter
        FOREIGN KEY (reporter_uuid) REFERENCES users(uuid)
);

CREATE INDEX idx_reports_project_id ON reports(project_id);
CREATE INDEX idx_reports_date ON reports(report_date);

------------------------------------------------------------
-- FORM TEMPLATE
------------------------------------------------------------
CREATE TABLE form_templates (
    id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    form_template_id  TEXT UNIQUE NOT NULL,
    form_name         TEXT NOT NULL,
    form_description  TEXT,
    form_status       TEXT,
    mandatory_forms   TEXT,
    optional_forms    TEXT,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

------------------------------------------------------------
-- COMPLETED FORM
------------------------------------------------------------
CREATE TABLE completed_forms (
    id                 UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    completed_form_id  TEXT UNIQUE NOT NULL,
    report_id          TEXT NOT NULL,
    form_template_id   TEXT NOT NULL,
    form_data          TEXT,
    created_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT fk_completed_forms_report
        FOREIGN KEY (report_id) REFERENCES reports(report_id),
    CONSTRAINT fk_completed_forms_template
        FOREIGN KEY (form_template_id) REFERENCES form_templates(form_template_id)
);

CREATE INDEX idx_completed_forms_report ON completed_forms(report_id);
CREATE INDEX idx_completed_forms_template ON completed_forms(form_template_id);

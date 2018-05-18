import models


def create_api(app):
    models.db.init_app(app)
    models.create_models(app, "/api/v1")

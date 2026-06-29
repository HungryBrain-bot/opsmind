from backend.app.config.settings import settings
from backend.app.factory import create_app

app = create_app(settings)

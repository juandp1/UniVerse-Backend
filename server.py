from start.app import app
from config.server import server_config

if __name__ == "__main__":
    app.config.from_object(server_config["development"])
    app.run()

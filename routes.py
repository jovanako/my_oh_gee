def create_routes(app):
  
  @app.get("/")
  def home():
    return "Oh Gee!"

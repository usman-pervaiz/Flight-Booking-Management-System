from app import app
from app.models import db

if __name__ == "__main__":
    #db.drop_all()
    db.create_all()
    app.run(debug=True)
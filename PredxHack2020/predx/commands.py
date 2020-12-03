from predx import db
from predx.models import User,Post
def create_table(app):
    db.create_all()
    db.commit()
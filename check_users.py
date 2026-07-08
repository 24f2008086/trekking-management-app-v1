from app import app
from models import User

with app.app_context():
    users = User.query.all()

    print("\n===== USERS =====")
    for user in users:
        print(
            user.id,
            user.name,
            user.email,
            user.role,
            user.status
        )
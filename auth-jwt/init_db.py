from app import app, db
from models.user import User
from werkzeug.security import generate_password_hash

def create_admin():
    with app.app_context():
        db.create_all()  # Garante que as tabelas sejam criadas

        # Verifica se o usuário admin já existe
        if not User.query.filter_by(email='admin@email.com').first():
            admin = User(
                name='Admin', 
                email='admin@email.com', 
                password=generate_password_hash('admin123'), 
                role='ADMIN'
            )
            db.session.add(admin)
            db.session.commit()
            print("Usuário ADMIN criado com sucesso!")
        else:
            print("Usuário ADMIN já existe.")

if __name__ == "__main__":
    create_admin()
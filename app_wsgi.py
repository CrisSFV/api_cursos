# Punto de entrada WSGI para Gunicorn
# Este archivo es el que Gunicorn ejecutará

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()

from flask import Flask, request, redirect, render_template_string
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import os

# Configuración
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Base de datos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False, unique=True)
    contrasena_hash = db.Column(db.String(200), nullable=False)

# Crear la base de datos
with app.app_context():
    db.create_all()

# HTML sencillo para registrar/iniciar sesión
HTML = """
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
  <h2>{{ titulo }}</h2>
  <form method="post">
    <input name="usuario" placeholder="Nombre de usuario" required><br><br>
    <input name="contrasena" placeholder="Contraseña" type="password" required><br><br>
    <input type="submit" value="{{ boton }}">
  </form>
  <br>
  <a href="/">Inicio</a> | <a href="/registrar">Registrar</a> | <a href="/login">Login</a>
</body>
</html>
"""

@app.route("/")
def inicio():
    
    return "<h1>Bienvenido al sistema de usuarios</h1><p><a href='/registrar'>Registrar</a> | <a href='/login'>Login</a></p>"

@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        usuario = request.form["usuario"]
        contrasena = request.form["contrasena"]
        hash_pw = bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt()).decode()

        if Usuario.query.filter_by(nombre=usuario).first():
            return "❌ El usuario ya existe."

        nuevo_usuario = Usuario(nombre=usuario, contrasena_hash=hash_pw)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return "✅ Usuario registrado correctamente."

    return render_template_string(HTML, titulo="Registrar Usuario", boton="Registrar")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        contrasena = request.form["contrasena"]
        user = Usuario.query.filter_by(nombre=usuario).first()
        if user and bcrypt.checkpw(contrasena.encode(), user.contrasena_hash.encode()):
            return f"✅ Bienvenido, {usuario}"
        return "❌ Usuario o contraseña incorrectos."

    return render_template_string(HTML, titulo="Iniciar Sesión", boton="Entrar")

# Ejecutar en puerto 5800
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5800)
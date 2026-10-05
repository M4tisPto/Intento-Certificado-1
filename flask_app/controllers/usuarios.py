from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.usuario import Usuario
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registrar", methods=["POST"])

def registrar():
    if not Usuario.validate_register(request.form):
        return redirect("/")
    datos = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "email": request.form['email'],
        "password": request.form['password']
    }
    usuario_id = Usuario.save(datos)
    session['usuario_id'] = usuario_id
    return redirect("/cine")

@app.route("/login", methods=["POST"])
def login():
    datos = {"email": request.form['email']}
    usuario = Usuario.get_by_email(datos)
    if not usuario:
        flash("E-mail inválido", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash("Contraseña inválida", "login")
        return redirect("/")
    session['usuario_id'] = usuario.id
    return redirect("/cine")

@app.route("/cine")

def cine():
    
    if 'usuario_id' not in session:
        return redirect("/")
    datos = {"id": session['usuario_id']}
    usuario = Usuario.get_by_id(datos)
    return render_template("cine.html", usuario=usuario)
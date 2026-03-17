from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "clave_secreta_super_segura"

@app.route("/")
def index():
    return render_template("index.html", title="Inicio")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        usuario = request.form.get("username")
        contraseña = request.form.get("password")

        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (username, password, role) VALUES (?, ?, ?)",
                           (usuario, generate_password_hash(contraseña), "user"))
            conn.commit()
            flash(f"Usuario {usuario} registrado con éxito!", "success")
        except sqlite3.IntegrityError:
            flash("Ese usuario ya existe.", "error")
        finally:
            conn.close()
        return redirect(url_for("login"))
    return render_template("register.html", title="Registro")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("username")
        contraseña = request.form.get("password")

        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password, role FROM usuarios WHERE username=?", (usuario,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado and check_password_hash(resultado[0], contraseña):
            session["usuario"] = usuario
            session["role"] = resultado[1]   # guarda el rol en la sesión
            flash("Login exitoso!", "success")
            return redirect(url_for("perfil"))
        else:
            flash("Usuario o contraseña incorrectos", "error")
            return redirect(url_for("login"))
    return render_template("login.html", title="Login")

@app.route("/perfil")
def perfil():
    if "usuario" in session:
        return render_template("perfil.html", title="Perfil")
    return redirect(url_for("login"))

@app.route("/configuracion")
def configuracion():
    if "usuario" in session:
        return render_template("configuracion.html", title="Configuración")
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if "usuario" in session and session.get("role") == "admin":
        return render_template("dashboard.html", title="Dashboard")
    flash("Acceso denegado. Solo administradores.", "error")
    return redirect(url_for("index"))

@app.route("/editor")
def editor():
    if "usuario" in session and session.get("role") in ["admin", "editor"]:
        return render_template("editor.html", title="Editor")
    flash("Acceso denegado. Solo editores o administradores.", "error")
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    session.pop("role", None)
    flash("Sesión cerrada.", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)

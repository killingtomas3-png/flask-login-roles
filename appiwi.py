from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = "clave_secreta_super_segura"

# --- Funciones auxiliares ---
def get_db_connection():
    conn = sqlite3.connect("usuarios.db")
    conn.row_factory = sqlite3.Row
    return conn

def role_required(roles):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "role" not in session or session["role"] not in roles:
                flash("Acceso denegado", "danger")
                return redirect(url_for("login"))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

# --- Rutas principales ---
@app.route("/")
def index():
    return render_template("index.html", title="Inicio")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        usuario = request.form.get("username")
        contraseña = request.form.get("password")

        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO usuarios (username, password, role) VALUES (?, ?, ?)",
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

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password, role FROM usuarios WHERE username=?", (usuario,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado and check_password_hash(resultado[0], contraseña):
            session["usuario"] = usuario
            session["role"] = resultado[1]
            flash("Login exitoso!", "success")
            if session["role"] == "admin":
                return redirect(url_for("dashboard"))
            elif session["role"] == "editor":
                return redirect(url_for("editor"))
            else:
                return redirect(url_for("perfil"))
        else:
            flash("Usuario o contraseña incorrectos", "error")
            return redirect(url_for("login"))
    return render_template("login.html", title="Login")

@app.route("/perfil")
@role_required(["admin", "editor", "user"])
def perfil():
    return render_template("perfil.html", title="Perfil")

@app.route("/dashboard")
@role_required(["admin"])
def dashboard():
    conn = get_db_connection()
    total_usuarios = conn.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
    total_admins = conn.execute("SELECT COUNT(*) FROM usuarios WHERE role='admin'").fetchone()[0]
    total_editores = conn.execute("SELECT COUNT(*) FROM usuarios WHERE role='editor'").fetchone()[0]
    conn.close()
    return render_template("dashboard.html",
                           title="Dashboard",
                           total_usuarios=total_usuarios,
                           total_admins=total_admins,
                           total_editores=total_editores)

@app.route("/editor")
@role_required(["admin", "editor"])
def editor():
    return render_template("editor.html", title="Editor")

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    session.pop("role", None)
    flash("Sesión cerrada.", "info")
    return redirect(url_for("login"))

# --- CRUD de usuarios ---
@app.route("/usuarios")
@role_required(["admin"])
def usuarios():
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM usuarios").fetchall()
    conn.close()
    return render_template("usuarios.html", users=users)

@app.route("/usuarios/nuevo", methods=["GET", "POST"])
@role_required(["admin"])
def nuevo_usuario():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        role = request.form["role"]

        conn = get_db_connection()
        conn.execute("INSERT INTO usuarios (username, password, role) VALUES (?, ?, ?)",
                     (username, password, role))
        conn.commit()
        conn.close()
        flash("Usuario creado correctamente", "success")
        return redirect(url_for("usuarios"))
    return render_template("nuevo_usuario.html")

@app.route("/usuarios/eliminar/<int:id>")
@role_required(["admin"])
def eliminar_usuario(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM usuarios WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash("Usuario eliminado", "danger")
    return redirect(url_for("usuarios"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # cambiá el puerto si 5000 está ocupado

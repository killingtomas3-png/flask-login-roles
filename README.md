#  My Flask App with Glass UI

A modern web application built with **Flask**, featuring authentication, role-based access (admin, editor, user), a complete user CRUD, and a stylish **glassmorphism + animations** design .

---

##  Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/yourrepo.git
   cd yourrepo

    Install dependencies:
    bash

    pip install -r requirements.txt

    Initialize the database:
    bash

    sqlite3 usuarios.db

    Inside the SQLite prompt:
    sql

    CREATE TABLE usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    );
    .exit

▶ Run the App
bash

python appiwi.py

The app will run at:
 http://localhost:5001
 Features

    User registration and login with hashed passwords.

    Role-based access: admin, editor, user.

    Dashboard with user statistics.

    Full CRUD for users (create, list, delete).

    Modern glassmorphism UI with animations and hover effects.

    Responsive design with Bootstrap integration.

#  Mi App Flask con Glass UI

Una aplicación web hecha en **Flask** con autenticación, roles (admin, editor, user), CRUD de usuarios y un diseño moderno estilo **glass + animaciones** .

---

##  Instalación

1. Cloná el repo:
   ```bash
   git clone https://github.com/tuusuario/tu-repo.git
   cd tu-repo
2  Instalá dependencias:
    bash

    pip install -r requirements.txt

3    Inicializá la base de datos:
    bash

    sqlite3 usuarios.db

4    Dentro del prompt de SQLite:
    sql

    CREATE TABLE usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    );
    .exit

▶ Ejecución
bash

python appiwi.py

La app corre en:
 http://localhost:5001
 Funcionalidades

    Registro y login con contraseñas hasheadas.

    Roles: admin, editor, user.

    Dashboard con métricas de usuarios.

    CRUD completo de usuarios (crear, listar, eliminar).

    Estilo glass moderno con animaciones y fuentes atractivas.
 Autor

Proyecto creado por Tomas, con mucho amor y pasión por el código 
:3



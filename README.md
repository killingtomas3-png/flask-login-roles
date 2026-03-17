# Flask Login con Roles

Sistema web en **Flask** que implementa:
- Registro y login de usuarios con contraseñas encriptadas.
- Roles (`admin`, `editor`, `user`) guardados en sesión.
- Menú dinámico según el rol.
- Rutas protegidas: Dashboard (solo admin) y Editor (admin/editor).
- Mensajes flash para feedback de usuario.

## 🚀 Instalación
```bash
git clone https://github.com/tomas/flask-login-roles.git
cd flask-login-roles
pip install -r requirements.tx
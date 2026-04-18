# 🚀 ACCESO A RDS - GUÍA RÁPIDA

## ⚠️ IMPORTANTE

Tu máquina local **NO PUEDE** conectar directamente a RDS (firewall bloquea puerto 3306).

**SOLUCIÓN:** Usar **EC2** como intermediario vía AWS Systems Manager.

---

## ✅ FORMA RECOMENDADA (3 pasos)

### 1️⃣ Abre cmder y conecta a EC2

```powershell
aws ssm start-session --target i-04c1387964094f50e --region us-east-1
```

Verás:
```
sh-4.2$
```

### 2️⃣ Una vez dentro de EC2, ejecuta cualquiera de estos comandos:

**Ver todas las bases de datos:**
```bash
python3 -c 'import mysql.connector; c=mysql.connector.connect(host="db-prueba82.cozu8wwe6bt6.us-east-1.rds.amazonaws.com",user="admin",password="Prueba82!"); cur=c.cursor(); cur.execute("SHOW DATABASES;"); [print(f"  ✓ {t[0]}") for t in cur.fetchall()]; c.close()'
```

**Ver tablas en app_db:**
```bash
python3 -c 'import mysql.connector; c=mysql.connector.connect(host="db-prueba82.cozu8wwe6bt6.us-east-1.rds.amazonaws.com",user="admin",password="Prueba82!",database="app_db"); cur=c.cursor(); cur.execute("SHOW TABLES;"); [print(f"  ✓ {t[0]}") for t in cur.fetchall()]; c.close()'
```

**Ver estructura de categories:**
```bash
python3 -c 'import mysql.connector; c=mysql.connector.connect(host="db-prueba82.cozu8wwe6bt6.us-east-1.rds.amazonaws.com",user="admin",password="Prueba82!",database="app_db"); cur=c.cursor(); cur.execute("DESCRIBE categories;"); [print(f"  {str(t[0]):20} {str(t[1]):30}") for t in cur.fetchall()]; c.close()'
```

**Ver estructura de courses:**
```bash
python3 -c 'import mysql.connector; c=mysql.connector.connect(host="db-prueba82.cozu8wwe6bt6.us-east-1.rds.amazonaws.com",user="admin",password="Prueba82!",database="app_db"); cur=c.cursor(); cur.execute("DESCRIBE courses;"); [print(f"  {str(t[0]):20} {str(t[1]):30}") for t in cur.fetchall()]; c.close()'
```

### 3️⃣ Salir de EC2
```bash
exit
```

---

## 🔑 DATOS DE CONEXIÓN

```
Host:     db-prueba82.cozu8wwe6bt6.us-east-1.rds.amazonaws.com
Puerto:   3306
Usuario:  admin
Pass:     Prueba82!
BD:       app_db
Engine:   MySQL 8.4.8
```

---

## 📊 TABLAS EN app_db

### categories
- id (INT, PK)
- name (VARCHAR 120)
- description (VARCHAR 500)
- created_at (DATETIME)

### courses
- id (INT, PK)
- nombre (VARCHAR 200)
- descripcion (TEXT)
- precio (FLOAT)
- categoria_id (INT, FK→categories.id)

---

## 🐍 Usar en Python/Flask

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:Prueba82!@db-prueba82.cozu8wwe6bt6.us-east-1.rds.amazonaws.com:3306/app_db'

db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run()
```

---

## 🎯 ARCHIVOS NUEVOS EN PROYECTO

| Archivo | Uso |
|---|---|
| `rds_utils.py` | Módulo Python (para cuando tengas acceso directo) |
| `ec2_rds_query.py` | Helper para mostrar comandos EC2 |
| `rds_query.ps1` | PowerShell helper |
| `RDS_ACCESO.md` | Documentación completa |
| `QUICK_START.md` | Esta guía rápida |

---

## 💡 TIPS

- **Copiar comandos:** Click derecho en cmder → Copy from buffer
- **Pegar comandos:** Click derecho → Paste
- **Long output:** Aumentar buffer en cmder settings
- **Timeout:** Si tarda mucho, presiona `Ctrl+C`

---

**Última actualización:** 10 Abril 2026 ✅


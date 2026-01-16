# ProjectScaffold

**ProjectScaffold** is a Python package that generates full-stack project scaffolds with a ready-to-use **MVC structure**, backend, frontend, and database templates.

With this tool, you can quickly create new projects in **Flask, Django, FastAPI, Node.js, Express, Spring Boot** for backend and **React, Vue, Angular, Svelte, Vanilla JS** for frontend, plus database setup for **SQLite, PostgreSQL, MySQL, MongoDB**.

---

## ⚡ Features

- Interactive CLI to select backend, frontend, and database
- Creates MVC folder structure:
  - `models/`
  - `views/`
  - `controllers/`
- Copies backend & frontend starter templates automatically
- Database templates included
- Overwrite protection to prevent accidental project replacement
- Ready-to-use starter files for Python MVC projects
- Cross-platform: Windows, Linux, macOS
- Fully tested with `pytest` and `flake8`

---

## 🛠 Installation

```bash
# Recommended: Use virtual environment
pip install projectscaffold
```

git clone https://github.com/maria2021831011/ProjectScaffold.git
cd ProjectScaffold
pip install -e .


## 🚀 Usage

Run the CLI:project-scaffold

Project name: DemoApp
Backend: flask
Frontend: react
DB: sqlite

DemoApp/
├─ backend/
├─ frontend/
├─ db/
├─ models/
├─ views/
├─ controllers/
└─ README.md


## 📁 Supported Backends

* Flask
* Django
* FastAPI
* Node.js
* Express
* Spring Boot

## 📁 Supported Frontends

* Vanilla JS
* React
* Vue
* Angular
* Svelte

## 🗄 Supported Databases

* SQLite
* PostgreSQL
* MySQL
* MongoDB

## 🔧 Development

Install dev dependencies:

pip install -r requirements_dev.txt

flake8 src tests

pytest

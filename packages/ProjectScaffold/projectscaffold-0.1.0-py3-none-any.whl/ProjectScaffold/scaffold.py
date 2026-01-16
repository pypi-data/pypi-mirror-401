import shutil
from pathlib import Path

# Base templates folder
BASE_DIR = Path(__file__).resolve().parent / "templates"

# Backend templates
BACKEND_TEMPLATES = {
    "flask": BASE_DIR / "backend/flask_template",
    "django": BASE_DIR / "backend/django_template",
    "fastapi": BASE_DIR / "backend/fastapi_template",
    "nodejs": BASE_DIR / "backend/nodejs_template",
    "express": BASE_DIR / "backend/express_template",
    "springboot": BASE_DIR / "backend/springboot_template",
}

# Frontend templates
FRONTEND_TEMPLATES = {
    "vanilla": BASE_DIR / "frontend/vanilla_template",
    "react": BASE_DIR / "frontend/react_template",
    "vue": BASE_DIR / "frontend/vue_template",
    "angular": BASE_DIR / "frontend/angular_template",
    "svelte": BASE_DIR / "frontend/svelte_template",
}

# DB templates
DB_TEMPLATES = {
    "sqlite": BASE_DIR / "db/sqlite.sql",
    "postgres": BASE_DIR / "db/postgres.sql",
    "mysql": BASE_DIR / "db/mysql.sql",
    "mongodb": BASE_DIR / "db/mongodb_template.json",
}


def copy_template(src: Path, dst: Path) -> None:
    """Copy a file or directory recursively"""
    if src.is_dir():
        shutil.copytree(src, dst)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def create_project(name: str, backend: str, frontend: str, db: str) -> None:
    """Create project structure with selected backend, frontend, and db"""
    root = Path.cwd() / name

    # Overwrite protection
    if root.exists():
        raise FileExistsError(f"Project '{name}' already exists")

    root.mkdir()

    # Create MVC folders
    for folder in ["models", "views", "controllers"]:
        (root / folder).mkdir()

    # Copy backend template
    backend_template = BACKEND_TEMPLATES[backend]
    copy_template(backend_template, root / "backend")

    # Copy frontend template
    frontend_template = FRONTEND_TEMPLATES[frontend]
    copy_template(frontend_template, root / "frontend")

    # Copy DB template
    db_dir = root / "db"
    db_dir.mkdir()
    db_template = DB_TEMPLATES[db]
    copy_template(db_template, db_dir / db_template.name)

    # Starter MVC files
    (root / "models/user.py").write_text("class User:\n    pass\n")
    (root / "views/user_view.py").write_text(
        "def show_user(user):\n    return str(user)\n"
    )
    (root / "controllers/user_controller.py").write_text(
        "from models.user import User\n"
    )

    # Root README
    (root / "README.md").write_text(
        f"# {name}\n\nGenerated with ProjectScaffold\n"
    )

    # Success message
    print(
        f"Scaffolded {name} with {backend} backend, "
        f"{frontend} frontend, and {db} database."
     )

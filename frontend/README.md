# AgriTech Frontend (Django)

This is the flat-structured Django frontend for the AgriTech platform.

## Project Structure


- **`manage.py`**: Entry point for administrative tasks.
- **`settings.py`**: Project settings.
- **`urls.py`**: Main URL routing.
- **`views.py`**: View logic.
- **`templates/`**: HTML templates.
- **`static/`**: Static assets (CSS, Images).
- **`db.sqlite3`**: Local database.

## How to Run Locally

To start the development server, run:

```bash
python manage.py runserver
```

The platform will be available at:
- **Home (New Design)**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Old Dashboard**: [http://127.0.0.1:8000/old-dashboard/](http://127.0.0.1:8000/old-dashboard/)

## Design Notes
The root URL (`/`) now serves the **Agritecture** design (glassmorphism/premium look). The original dashboard has been moved to `/old-dashboard/`.

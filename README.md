# School Lost & Found Tracker

Simple Flask application to report and track lost items at a school. Users can submit a report with student name, class, where to return the item, a picture, and the return status. Blue/white theme and easy to use UI.

## Features
- Submit new lost item reports with image upload
- View list of reports with search/filter by status
- Update status (e.g., Reported, Found, Returned)
- Serve uploaded images securely

## Quickstart
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app
export FLASK_ENV=development
python app/db_init.py  # initialize the SQLite database
flask run --host=0.0.0.0 --port=8000
```

Open http://localhost:8000

## Project Structure
```
app/
  __init__.py
  routes.py
  db.py
  db_init.py
  static/
    css/
      styles.css
    uploads/
  templates/
    base.html
    list.html
    create.html
requirements.txt
README.md
```

## Environment Variables
- `UPLOAD_FOLDER` (optional): Directory for uploads. Defaults to `app/static/uploads`.

## Notes
- Uploaded images are saved with unique filenames.
- Max upload size is limited to 5 MB by default.


import os
import uuid
from typing import List, Tuple
from flask import request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename

from . import app
from .db import get_db, close_db

ALLOWED_EXTENSIONS: Tuple[str, ...] = ('.png', '.jpg', '.jpeg', '.gif', '.webp')
VALID_STATUSES: Tuple[str, ...] = ('REPORTED', 'FOUND', 'RETURNED')


@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)


def _is_allowed_file(filename: str) -> bool:
    lower = filename.lower()
    return any(lower.endswith(ext) for ext in ALLOWED_EXTENSIONS)


@app.route('/')
def index():
    status = request.args.get('status', '').upper().strip()
    query = request.args.get('q', '').strip()
    params: List[str] = []
    where: List[str] = []

    if status and status in VALID_STATUSES:
        where.append('status = ?')
        params.append(status)

    if query:
        where.append('(person_name LIKE ? OR class_name LIKE ? OR return_location LIKE ?)')
        like = f"%{query}%"
        params.extend([like, like, like])

    sql = 'SELECT * FROM lost_items'
    if where:
        sql += ' WHERE ' + ' AND '.join(where)
    sql += ' ORDER BY created_at DESC'

    conn = get_db()
    rows = conn.execute(sql, params).fetchall()
    items = [dict(row) for row in rows]
    return render_template('list.html', items=items, statuses=VALID_STATUSES, active_status=status, q=query)


@app.route('/new', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        person_name = request.form.get('person_name', '').strip()
        class_name = request.form.get('class_name', '').strip()
        return_location = request.form.get('return_location', '').strip()
        status = request.form.get('status', 'REPORTED').upper().strip()
        status = status if status in VALID_STATUSES else 'REPORTED'

        if not person_name or not class_name or not return_location:
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('create'))

        image_filename = None
        if 'picture' in request.files:
            file = request.files['picture']
            if file and file.filename:
                if not _is_allowed_file(file.filename):
                    flash('Invalid image type. Allowed: png, jpg, jpeg, gif, webp', 'error')
                    return redirect(url_for('create'))
                base_name = secure_filename(file.filename)
                uuid_str = uuid.uuid4().hex
                ext = os.path.splitext(base_name)[1].lower()
                filename = f"{uuid_str}{ext}"
                upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(upload_path)
                image_filename = filename

        conn = get_db()
        conn.execute(
            'INSERT INTO lost_items (person_name, class_name, return_location, image_filename, status) VALUES (?, ?, ?, ?, ?)',
            (person_name, class_name, return_location, image_filename, status),
        )
        conn.commit()
        flash('Report submitted successfully.', 'success')
        return redirect(url_for('index'))

    return render_template('create.html', statuses=VALID_STATUSES)


@app.route('/item/<int:item_id>/status', methods=['POST'])
def update_status(item_id: int):
    new_status = request.form.get('status', '').upper().strip()
    if new_status not in VALID_STATUSES:
        flash('Invalid status selected.', 'error')
        return redirect(url_for('index'))

    conn = get_db()
    conn.execute('UPDATE lost_items SET status = ? WHERE id = ?', (new_status, item_id))
    conn.commit()
    flash('Status updated.', 'success')
    return redirect(request.referrer or url_for('index'))
from flask import render_template, request, redirect, url_for, flash, send_file
from flask_login import login_user, login_required, logout_user
import bcrypt
import uuid
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from app import app
from app.db import get_db
from app.models import User
from app.utils import validate_contact_info

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        
        conn = get_db()
        user_row = conn.execute('SELECT * FROM user WHERE email = ?', (email,)).fetchone()

        if not user_row and email == 'admin@casadeapostas.com' and password.decode('utf-8') == 'admin123':
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())
            new_id = str(uuid.uuid4())
            conn.execute('INSERT INTO user (id, email, password) VALUES (?, ?, ?)', (new_id, email, hashed))
            conn.commit()
            user_row = {'id': new_id, 'email': email, 'password': hashed}
        
        if user_row and bcrypt.checkpw(password, user_row['password']):
            login_user(User(user_row['id'], user_row['email']))
            return redirect(url_for('dashboard'))
        else:
            error = "Credenciais inválidas."
            
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def home():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    clients = conn.execute('SELECT * FROM client ORDER BY registration_date DESC').fetchall()
    return render_template('dashboard.html', clients=clients)

@app.route('/report')
@login_required
def report():
    conn = get_db()
    clients = conn.execute('SELECT * FROM client ORDER BY full_name ASC').fetchall()
    report_data = []
    for c in clients:
        contacts = conn.execute('SELECT * FROM contact WHERE client_id = ?', (c['id'],)).fetchall()
        report_data.append({'client': c, 'contacts': contacts})
    return render_template('report.html', report_data=report_data)

@app.route('/report/pdf')
@login_required
def report_pdf():
    conn = get_db()
    clients = conn.execute('SELECT * FROM client ORDER BY full_name ASC').fetchall()
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 50
    
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, "Relatório de Clientes e Contatos")
    y -= 30
    
    for c in clients:
        if y < 100:
            p.showPage()
            y = height - 50
            
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, f"Cliente: {c['full_name']} (Registrado em:  {c['registration_date']})")
        y -= 15
        p.setFont("Helvetica", 10)
        p.drawString(60, y, f"E-mail: {c['emails'] or '-'} | Tel: {c['phones'] or '-'}")
        y -= 20
        
        contacts = conn.execute('SELECT * FROM contact WHERE client_id = ?', (c['id'],)).fetchall()
        if contacts:
            p.setFont("Helvetica-Oblique", 10)
            p.drawString(60, y, "Contatos Vinculados:")
            y -= 15
            p.setFont("Helvetica", 10)
            for contact in contacts:
                if y < 50:
                    p.showPage()
                    y = height - 50
                p.drawString(70, y, f"• {contact['full_name']} | E-mail: {contact['emails'] or '-'} | Tel: {contact['phones'] or '-'}")
                y -= 15
        else:
            p.setFont("Helvetica-Oblique", 10)
            p.drawString(60, y, "Nenhum contato vinculado.")
            y -= 15
            
        y -= 10 
        p.line(50, y+5, width-50, y+5)
        y -= 15
        
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='relatorio_clientes.pdf', mimetype='application/pdf')

@app.route('/client/new', methods=['GET', 'POST'])
@login_required
def create_client():
    if request.method == 'POST':
        full_name = request.form['full_name']
        emails = request.form['emails']
        phones = request.form['phones']
        
        is_valid, error_msg = validate_contact_info(emails, phones)
        if not is_valid:
            flash(error_msg, 'error')
            client_data = {'full_name': full_name, 'emails': emails, 'phones': phones}
            return render_template('client.html', action="Criar", client=client_data)

        client_id = str(uuid.uuid4())
        reg_date = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        conn = get_db()
        conn.execute('INSERT INTO client (id, full_name, emails, phones, registration_date) VALUES (?, ?, ?, ?, ?)',
                     (client_id, full_name, emails, phones, reg_date))
        conn.commit()
        flash('Cliente criado com sucesso!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('client.html', action="Criar", client=None)

@app.route('/client/<id>', methods=['GET', 'POST'])
@login_required
def edit_client(id):
    conn = get_db()
    if request.method == 'POST':
        full_name = request.form['full_name']
        emails = request.form['emails']
        phones = request.form['phones']
        
        is_valid, error_msg = validate_contact_info(emails, phones)
        if not is_valid:
            flash(error_msg, 'error')
            client_data = {'id': id, 'full_name': full_name, 'emails': emails, 'phones': phones}
            contacts = conn.execute('SELECT * FROM contact WHERE client_id = ?', (id,)).fetchall()
            return render_template('client.html', action="Editar", client=client_data, contacts=contacts)

        conn.execute('UPDATE client SET full_name = ?, emails = ?, phones = ? WHERE id = ?',
                     (full_name, emails, phones, id))
        conn.commit()
        flash('Cliente atualizado com sucesso!', 'success')
        return redirect(url_for('dashboard'))
        
    client = conn.execute('SELECT * FROM client WHERE id = ?', (id,)).fetchone()
    contacts = conn.execute('SELECT * FROM contact WHERE client_id = ?', (id,)).fetchall()
    return render_template('client.html', action="Editar", client=client, contacts=contacts)

@app.route('/client/<id>/delete', methods=['POST'])
@login_required
def delete_client(id):
    conn = get_db()
    conn.execute('PRAGMA foreign_keys = ON')
    conn.execute('DELETE FROM client WHERE id = ?', (id,))
    conn.commit()
    flash('Cliente excluído com sucesso!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/client/<client_id>/contact/new', methods=['GET', 'POST'])
@login_required
def create_contact(client_id):
    if request.method == 'POST':
        full_name = request.form['full_name']
        emails = request.form['emails']
        phones = request.form['phones']
        
        is_valid, error_msg = validate_contact_info(emails, phones)
        if not is_valid:
            flash(error_msg, 'error')
            client = get_db().execute('SELECT full_name FROM client WHERE id = ?', (client_id,)).fetchone()
            contact_data = {'full_name': full_name, 'emails': emails, 'phones': phones}
            return render_template('contact.html', action="Criar", contact=contact_data, client_id=client_id, client_name=client['full_name'])

        contact_id = str(uuid.uuid4())
        conn = get_db()
        conn.execute('INSERT INTO contact (id, client_id, full_name, emails, phones) VALUES (?, ?, ?, ?, ?)',
                     (contact_id, client_id, full_name, emails, phones))
        conn.commit()
        flash('Contato adicionado com sucesso!', 'success')
        return redirect(url_for('edit_client', id=client_id))
        
    client = get_db().execute('SELECT full_name FROM client WHERE id = ?', (client_id,)).fetchone()
    return render_template('contact.html', action="Criar", contact=None, client_id=client_id, client_name=client['full_name'])

@app.route('/contact/<id>', methods=['GET', 'POST'])
@login_required
def edit_contact(id):
    conn = get_db()
    if request.method == 'POST':
        full_name = request.form['full_name']
        emails = request.form['emails']
        phones = request.form['phones']
        
        is_valid, error_msg = validate_contact_info(emails, phones)
        if not is_valid:
            flash(error_msg, 'error')
            contact_data = {'id': id, 'full_name': full_name, 'emails': emails, 'phones': phones}
            contact_db = conn.execute('SELECT client_id FROM contact WHERE id = ?', (id,)).fetchone()
            client = conn.execute('SELECT full_name FROM client WHERE id = ?', (contact_db['client_id'],)).fetchone()
            return render_template('contact.html', action="Editar", contact=contact_data, client_id=contact_db['client_id'], client_name=client['full_name'])

        conn.execute('UPDATE contact SET full_name = ?, emails = ?, phones = ? WHERE id = ?',
                     (full_name, emails, phones, id))
        conn.commit()
        flash('Contato atualizado com sucesso!', 'success')
        contact = conn.execute('SELECT client_id FROM contact WHERE id = ?', (id,)).fetchone()
        return redirect(url_for('edit_client', id=contact['client_id']))
        
    contact = conn.execute('SELECT * FROM contact WHERE id = ?', (id,)).fetchone()
    client = conn.execute('SELECT full_name FROM client WHERE id = ?', (contact['client_id'],)).fetchone()
    return render_template('contact.html', action="Editar", contact=contact, client_id=contact['client_id'], client_name=client['full_name'])

@app.route('/contact/<id>/delete', methods=['POST'])
@login_required
def delete_contact(id):
    conn = get_db()
    contact = conn.execute('SELECT client_id FROM contact WHERE id = ?', (id,)).fetchone()
    conn.execute('DELETE FROM contact WHERE id = ?', (id,))
    conn.commit()
    return redirect(url_for('edit_client', id=contact['client_id']))

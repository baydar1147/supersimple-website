from flask import Flask, render_template, request, redirect, url_for, flash
import json
import datetime
from crm import CRM, Musteri

app = Flask(__name__)
app.secret_key = "mysecretkey"

crm = CRM()

@app.route('/')
def index():
    return render_template('index.html', customers=crm.musterileri_listele())

@app.route('/add', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        ad = request.form['ad']
        telefon = request.form['telefon']
        ulke = request.form['ulke']
        notlar = request.form['notlar']
        borc = float(request.form['borc'])
        crm.musteri_ekle(ad, telefon, ulke, notlar, borc)
        flash('Müşteri başarıyla eklendi!')
        return redirect(url_for('index'))
    return render_template('add_customer.html')

@app.route('/delete/<int:id>')
def delete_customer(id):
    crm.musteri_sil(id)
    flash('Müşteri başarıyla silindi!')
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_customer(id):
    musteri = next((m for m in crm.musteriler if m.musteri_id == id), None)
    if request.method == 'POST':
        ad = request.form['ad']
        telefon = request.form['telefon']
        ulke = request.form['ulke']
        notlar = request.form['notlar']
        borc = float(request.form['borc'])
        crm.musteri_guncelle(id, ad, telefon, ulke, notlar, borc)
        flash('Müşteri başarıyla güncellendi!')
        return redirect(url_for('index'))
    return render_template('update_customer.html', customer=musteri)

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', customers=crm.musterileri_listele())

if __name__ == '__main__':
    app.run(debug=True)

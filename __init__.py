from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)                                                                                                                  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions
 
# Fonction pour créer une clé "authentifie" dans la session utilisateur
def est_authentifie():
    return session.get('authentifie')

def estauthentifie():
    return session.get('authentifier')

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/lecture')
def lecture():
    if not est_authentifie():
        # Rediriger vers la page d'authentification si l'utilisateur n'est pas authentifié
        return redirect(url_for('authentification'))

  # Si l'utilisateur est authentifié
    return "<h2>Bravo, vous êtes authentifié</h2>"
    
    if not estauthentifie():
        # Rediriger vers la page d'authentification si l'utilisateur n'est pas authentifié
        return redirect(url_for('authentification'))

  # Si l'utilisateur est authentifié
    return "<h2>Bravo, vous êtes authentifié pour user</h2>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        # Vérifier les identifiants
        if request.form['username'] == 'admin' and request.form['password'] == 'password': # password à cacher par la suite
            session['authentifie'] = True
            session['authentifier'] = False
            # Rediriger vers la route lecture après une authentification réussie
            return redirect(url_for('lecture'))

        elif request.form['username'] == 'user' and request.form['password'] == '12345': # password à cacher par la suite
            session['authentifier'] = True
            session['authentifie'] = False
            # Rediriger vers la route lecture après une authentification réussie
            return redirect(url_for('lecture'))
        else:
            # Afficher un message d'erreur si les identifiants sont incorrects
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/enregistrer_client', methods=['GET'])
def formulaire_client():
    return render_template('formulaire.html') 

@app.route('/enregistrer_client', methods=['POST'])
def enregistrer_client():
    nom = request.form['nom']
    prenom = request.form['prenom']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)', (1002938, nom, prenom, "ICI"))
    conn.commit()
    conn.close()
    return redirect('/consultation/')  
    

@app.route('/fiche_nom/<post_nom>')
def fiche_nom(post_nom):
     if estauthentifie():
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clients WHERE Nom = ?', (post_nom,))
        data = cursor.fetchall()
        conn.close()
        
        return render_template('read_data.html', data=data)

@app.route('/enregistrer_livres', methods=['GET', 'POST'])
def ajouter_livre():
    if not est_authentifie():
        return redirect(url_for('authentification'))

    if request.method == 'POST':
        titre = request.form['titre']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO livres (titre) VALUES (?)', (titre))
        conn.commit()
        conn.close()

        return redirect(url_for('dashboard_admin'))

    return render_template('formulaire_livres.html')
 
# Route pour les admins (gestion de la bibliothèque)
@app.route('/admin')
def dashboard_admin():
    if not est_authentifie():
        return redirect(url_for('authentification'))
    
    # Récupérer tous les livres depuis la base de données
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres')
    livres = cursor.fetchall()
    conn.close()
 
@app.route('/supprimer_livre/<int:id>')
def supprimer_livre(id):
    if not est_authentifie():
        return redirect(url_for('authentification'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM livres WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('dashboard_admin'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('authentification'))
                                                                                                                                       
if __name__ == "__main__":
  app.run(debug=True)

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

@app.route('/fiche_nom/<post_nom>')
def fiche_nom(post_nom):
     if estauthentifie():
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clients WHERE Nom = ?', (post_nom,))
        data = cursor.fetchall()
        conn.close()
        
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

    # Connexion à la base de données
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Exécution de la requête SQL pour insérer un nouveau client
    cursor.execute('INSERT INTO clients ( nom, prenom, adresse) VALUES ( ?, ?, ?)', ( nom, prenom, "ICI"))
    conn.commit()
    conn.close()
    return redirect('/consultation/')  # Rediriger vers la page d'accueil après l'enregistrement
    

@app.route('/enregistrer_livres', methods=['GET'])
def ajouter_livre():
    return render_template('formulaire_livres.html')

@app.route('/enregistrer_livres', methods=['POST'])
def enregistrer_livres():
        nom = request.form['nom']  
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO livres (nom) VALUES (?)', (nom,))
        conn.commit()
        conn.close()
 
        return redirect(url_for('consultation_livres'))


# Route pour les admins (gestion de la bibliothèque)
@app.route('/consultation_livres')
def consultation_livres():
    # Récupérer tous les livres depuis la base de données
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data_livres.html', data=data)
 
@app.route('/supprimer_livre/<lnom>')
def supprimer_livre(lnom):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM livres WHERE nom = ?', (lnom,))
    conn.commit()
    conn.close()

    return redirect(url_for('consultation_livres'))    
    

@app.route('/emprunt_livre', methods=['GET'])
def emprunt_livre():
    return render_template('formulaire_livres_emprunt.html')

@app.route('/emprunt_livre', methods=['POST'])
def emprunter_livre(): 
    if request.method == 'POST':
        user_id = request.form['user_id']
        livre_id = request.form['livre_id']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO emprunt (user_id, livre_id, return_date) VALUES (?, ?, ?)', (user_id, livre_id, "A définir"))
        conn.commit()
        conn.close()
        return redirect(url_for('consultation_livres_emprunt'))
    
# --- Nouvelle route pour retourner un livre ---
@app.route('/retourner/<int:livre_id>')
# def retourner_livre(livre_id):
#    if estauthentifie():
 #       client_id = session['user_id']
  #      conn = sqlite3.connect('database.db')
   #     cursor = conn.cursor()
#
 #       # Mettre à jour l'emprunt avec la date de retour
  #      cursor.execute('UPDATE emprunt SET date_retour = ? WHERE client_id = ? AND livre_id = ? AND date_retour IS NULL',(datetime.now(), client_id, livre_id))
   #     conn.commit()
    #    conn.close()
     #   return redirect(url_for('consultation_livres_emprunt'))

@app.route('/retourner_livre', methods=['POST'])
def retourner_livre():
    if request.method == 'POST':
        # Retrieve user_id and livre_id from the form data
        user_id = request.form.get('user_id')
        livre_id = request.form.get('livre_id')

        # Validate that user_id and livre_id are provided
        if not user_id or not livre_id:
            return jsonify({"error": "User ID and Book ID are required"}), 400

        try:
            # Get the current date and time to mark the return date
            return_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Connect to the SQLite database
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            # Update the 'return_date' in the 'emprunt' table to the current date for the specific user_id and livre_id
            cursor.execute(
                '''
                UPDATE emprunt 
                SET return_date = ? 
                WHERE user_id = ? AND livre_id = ? AND return_date = "A définir"
                ''', 
                (return_date, user_id, livre_id)
            )

            # Commit the transaction
            conn.commit()

            # Check if any rows were affected (to ensure the book was actually borrowed by this user)
            if cursor.rowcount == 0:
                return jsonify({"error": "No record found or book already returned"}), 404

            conn.close()

            # Return a success message as JSON
            return jsonify({"message": "Book returned successfully", "user_id": user_id, "livre_id": livre_id, "return_date": return_date}), 200

        except sqlite3.Error as e:
            # Handle any SQLite error
            return jsonify({"error": f"An error occurred: {e}"}), 500
         
@app.route('/consultation_livres_emprunt')
def consultation_livres_emprunt():
    # Récupérer tous les livres depuis la base de données
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM emprunt')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data_emprunt.html', data=data)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('authentification'))
                                                                                                                                       
if __name__ == "__main__":
  app.run(debug=True)

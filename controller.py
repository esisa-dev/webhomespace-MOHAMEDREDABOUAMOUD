from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from business import Business

#################################################
import logging

logger = logging.getLogger('myapp')
logger.setLevel(logging.INFO)

handler = logging.FileHandler('app.log')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
###########################################################

app = Flask(__name__)
app.secret_key = os.urandom(24)
currentPath=""

@app.route('/')
def application():
    return redirect(url_for('Login'))
@app.route('/signUpp')
def signUpp():
    return render_template('signUp.html')
@app.route('/Login')
def Login():
    return render_template('login.html')
@app.route('/index') 
def index():
    return render_template('index.html',dirs=Business.getDirectoriesall(session['username']))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['login']
        password = request.form['password']
        if Business.Authentication(username,password):
            
            session['username'] = username
            global currentPath
            currentPath=username
            flash('You were successfully logged in')
            logger.info(f'{username} logged in')
            path = session['username']
            return redirect(url_for('index'))
        flash('Invalid username or password')
        logger.warning(f'Invalid login attempt for user {username}')
    return redirect(url_for('Login'))

@app.route('/logout',methods=['GET', 'POST'])
def logout():
    username = session['username']
    global currentPath
    currentPath=""
    session.pop('username', None)
    flash('You were successfully logged out')
    logger.info(f'{username} logged out')
    return redirect(url_for('Login'))

@app.route('/signUp',methods=['GET', 'POST'])
def signUp():
    print("*********************************************")
    if request.method == 'POST':
        username = request.form['login']
        password = request.form['password']
        if Business.creation(username,password):
            session['username'] = username
            global currentPath
            currentPath=username
            flash('You were successfully signed up')
            logger.info(f'{username} signed up')
            path = session['username']
            return render_template('index.html',dirs=Business.getDirectoriesall(path))
        flash('Invalid username or password')
        logger.warning(f'Invalid sign up attempt for user {username}')
    return render_template('signUp.html',error_auth="failed")

@app.route('/Index', methods=['POST'])
def Index():
    global currentPath
    path = currentPath
    user=session['username']
    logger.info(f'{user} enter to {path}')
    if request.method == 'POST':
        button = request.form['button']
        if button == 'user':
            return render_template('index.html', dirs=Business.getDirectoriesall(path))
        elif button == 'directories':
            dirs = str(Business.getDirectories(path))
            return render_template('index.html',dirs=Business.getDirectories(path), var='nombre des dossiers : '+str(len(dirs)))
        elif button == 'files':
            files = str(Business.getFiles(path))
            return render_template('index.html',dirs=Business.getFiles(path), var='nombre des fichiers : '+str(len(files)))
        elif button == 'space':
            total = Business.total_size(path)
            return render_template('index.html',dirs=Business.getDirectoriesall(path), var='nombre Total : '+str(total)+" ko")
        elif button == 'logout':
            return redirect(url_for('logout'))
        else:
            currentPath=os.path.join(currentPath,button)
    return render_template('index.html',dirs=Business.getDirectoriesall(path))

@app.route('/download')
def download():
    if 'username' in session:
        # Ajouter le code pour le téléchargement
        username = session['username']
        flash('You have downloaded the file')
        logger.info(f'{username} downloaded the file')
        return redirect(url_for('index'))
    else:
        flash('You need to be logged in to download the file')
        logger.warning('Unauthenticated attempt to download file')
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
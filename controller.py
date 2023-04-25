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
    if request.method == 'POST':
        button = request.form['button']
        text=request.form['input']
        if button.split(' ')[0] == 'back':
            if(currentPath.find('/')!=-1):
                currentPath=currentPath[0:currentPath.rfind('/')]
                path=currentPath
                return render_template('index.html', dirs=Business.getDirectoriesall(path))
            else:
                path=currentPath
                return render_template('index.html', dirs=Business.getDirectoriesall(path))
        elif button.split(' ')[0] == 'user':
            currentPath=user
            path=currentPath
            return render_template('index.html', dirs=Business.getDirectoriesall(path))
        elif button.split(' ')[0] == 'directories':
            dirs = Business.getDirectories(path)
            return render_template('index.html',dirs=Business.getDirectories(path), var='nombre des dossiers : '+str(len(dirs)))
        elif button.split(' ')[0] == 'files':
            files = Business.getFiles(path)
            return render_template('index.html',dirs=Business.getFiles(path), var='nombre des fichiers : '+str(len(files)))
        elif button.split(' ')[0] == 'space':
            total = Business.total_size(path)
            return render_template('index.html',dirs=Business.getDirectoriesall(path), var='Espace disk utilise : '+str(total)+" ko")
        elif button.split(' ')[0] == 'logout':
            return redirect(url_for('logout'))
        elif button.split(' ')[0] == 'rechercher':
            if(currentPath.find('/')!=-1):
                dirs=Business.rechercher(currentPath[0:currentPath.find('/')],text)
            else:
                dirs=Business.rechercher(currentPath,text)
            if len(dirs)>0:
                return render_template('index.html', dirs=dirs)
        elif button.split(' ')[0] =='download':
            Business.downloadHome(user)
            flash('You have downloaded the file')
            logger.info(f'{user} downloaded the file')
        else:
            logger.info(f'{user} enter to view file {button}')
            if os.path.isfile(button.split(' ')[1]):
                return render_template('viewFile.html',file=button.split(' ')[0],content=Business.getContent(button.split(' ')[1]))
            else:
                currentPath=os.path.join(path,button.split(' ')[0])
                path=currentPath
    return render_template('index.html',dirs=Business.getDirectoriesall(path))
if __name__ == '__main__':
    app.run(debug=True)
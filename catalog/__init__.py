from flask import Flask, render_template, request, redirect, jsonify
from flask import Flask, url_for, flash
from sqlalchemy import create_engine, asc, desc, distinct
from sqlalchemy.orm import sessionmaker
from database_setup import User, Base, NovelsCategories, Items
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


app = Flask(__name__)


CLIENT_ID = json.loads(
    open('g_client_secret_.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"

# Connect to Database and create database session
engine = create_engine('sqlite:///novelscategories.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token for login
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('g_client_secret_.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps
                                 ('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # See if a user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px; height: 300px;border-radius:
    150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '''
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except BaseException:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = '''https://accounts.google.com/o/oauth2/revoke?
    token=%s''' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        # del login_session['access_token']
        # del login_session['gplus_id']
        # del login_session['username']
        # del login_session['email']
        # del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        print "this is the status " + result['status']
        response = make_response(json.dumps('''Failed to revoke token
        for given user.''', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view category and it's items Information
@app.route('/categories/<int:categories_id>/menu/JSON')
def categoriesMenuJSON(categories_id):
    categories = session.query(NovelsCategories).filter_by(
                id=categories_id).all()
    itemsMenu = session.query(Items).filter_by(
                categories_id=categories_id).all()
    return jsonify(Items=[i.serialize for i in itemsMenu])


# JSON to view Specific Category by id with its items Information by item id
@app.route('/categories/<int:categories_id>/menu/<int:menu_id>/JSON')
def categoryItemJSON(categories_id, menu_id):
    categories = session.query(NovelsCategories).filter_by(
                id=categories_id).all()
    Menu_Item = session.query(Items).filter_by(
                categories_id=categories_id, id=menu_id).one()
    return jsonify(Menu_Item=Menu_Item.serialize)


# JSON APIs to view all categories with their id
@app.route('/categories/JSON')
def catalogsJSON():
    catalogs = session.query(NovelsCategories).all()
    return jsonify(catalogs=[r.serialize for r in catalogs])


# Show all categories
@app.route('/')
@app.route('/categories/')
def showCategories():
    catalogs = session.query(NovelsCategories).order_by(
                asc(NovelsCategories.name))

    addedLast = session.query(NovelsCategories).order_by(
                desc(NovelsCategories.name)).limit(6)

    if 'username' not in login_session:
        return render_template('publiccatalogs.html',
                               catalogs=catalogs, addedLast=addedLast)
    else:
        return render_template('catalogs.html',
                               catalogs=catalogs, addedLast=addedLast)


# Create a new categories
@app.route('/categories/new/', methods=['GET', 'POST'])
def newCategories():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCategories = NovelsCategories(
                        name=request.form['name'],
                        user_id=login_session['user_id'])
        session.add(newCategories)
        flash('New categories %s Successfully Created' % newCategories.name)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategories.html')


# Create a about
@app.route('/categories/about/')
def showAbout():
    return render_template('about.html')


# Edit a catagories
@app.route('/categories/<int:categories_id>/edit/', methods=['GET', 'POST'])
def editCategories(categories_id):
    editCategories = session.query(
        NovelsCategories).filter_by(id=categories_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editCategories.user_id != login_session['user_id']:
        return '''<script>function myFunction() {alert('You are not authorized
        to edit this categories. Please create your own categories in order to
        edit.');}</script><body onload='myFunction()'>'''

    if request.method == 'POST':
        if request.form['name']:
            editCategories.name = request.form['name']
            flash('Categories Successfully Edited %s' % editCategories.name)
            return redirect(url_for('showCategories'))
    else:
        return render_template('editCategories.html',
                               categories=editCategories)


# Delete a catagories
@app.route('/categories/<int:categories_id>/delete/', methods=['GET', 'POST'])
def deleteCategories(categories_id):
    categoriesToDelete = session.query(
        NovelsCategories).filter_by(id=categories_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if categoriesToDelete.user_id != login_session['user_id']:
        return '''<script>function myFunction() {alert('You are not authorized
        to delete this categories. Please create your own categories in order
        to delete.');}</script><body onload='myFunction()'>'''

    if request.method == 'POST':
        session.delete(categoriesToDelete)
        flash('%s Successfully Deleted' % categoriesToDelete.name)
        session.commit()
        return redirect(url_for('showCategories', categories_id=categories_id))
    else:
        return render_template('deleteCategories.html',
                               categories=categoriesToDelete)


# show a category
@app.route('/categories/<int:categories_id>/')
@app.route('/categories/<int:categories_id>/menu/')
def showItemes(categories_id):
        categories = session.query(
                     NovelsCategories).filter_by(id=categories_id).one()
        itemsMenu = session.query(
                     Items).filter_by(categories_id=categories_id).all()
        creator = getUserInfo(categories.user_id)
        if 'username' not in login_session or creator.id != login_session[
                                                            'user_id']:
            return render_template('publicmenu.html', itemsMenu=itemsMenu,
                                   categories=categories, creator=creator)
        else:
            return render_template('menu.html', itemsMenu=itemsMenu,
                                   categories=categories, creator=creator)


# Create a new item
@app.route('/categories/<int:categories_id>/menu/new/',
           methods=['GET', 'POST'])
def newItemes(categories_id):
    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(NovelsCategories).filter_by(
                 id=categories_id).one()
    if login_session['user_id'] != categories.user_id:
        return '''<script>function myFunction() {alert('You are not authorized
         to add items to this catagories. Please create your own catagories in
         order to add items.');}</script><body onload='myFunction()'>'''
    if request.method == 'POST':
        newItem = Items(name=request.form['name'],
                        description=request.form['description'],
                        price=request.form['price'],
                        author=request.form['author'],
                        novelType=request.form['novelType'],
                        categories_id=categories_id,
                        user_id=categories.user_id)
        session.add(newItem)
        session.commit()
        flash('New %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showItemes', categories_id=categories_id))
    else:
        return render_template('newItemes.html', categories_id=categories_id)


# Edit Item
@app.route('/categories/<int:categories_id>/menu/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editItem(categories_id, menu_id):
    if 'username' not in login_session:
        return redirect('/login')

    editedItem = session.query(Items).filter_by(id=menu_id).one()
    categories = session.query(NovelsCategories).filter_by(
                                                id=categories_id).one()
    if login_session['user_id'] != categories.user_id:
        return '''<script>function myFunction() {alert('You are not authorized
         to edit items to this catagories. Please create your own catagories
         in order to edit items.');}</script><body onload='myFunction()'>'''
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['author']:
            editedItem.author = request.form['author']
        if request.form['novelType']:
            editedItem.novelType = request.form['novelType']
        session.add(editedItem)
        session.commit()
        flash('Item Successfully Edited')
        return redirect(url_for('showItemes', categories_id=categories_id))

    else:

        return render_template('editItem.html', categories_id=categories_id,
                               menu_id=menu_id, item=editedItem)


# Delete item
@app.route('/categories/<int:categories_id>/menu/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def deleteItem(categories_id, menu_id):
    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(
                 NovelsCategories).filter_by(id=categories_id).one()
    itemToDelete = session.query(Items).filter_by(id=menu_id).one()
    if login_session['user_id'] != categories.user_id:
        return '''<script>function myFunction() {alert('You are not authorized
        to delete items to this catagories. Please create your own catagories
        in order to delete items.');}</script><body onload='myFunction()'>'''
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('showItemes', categories_id=categories_id))
    else:
        return render_template('deleteItem.html', item=itemToDelete)


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['access_token']
            del login_session['gplus_id']
            del login_session['username']
            del login_session['email']
            del login_session['picture']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCategories'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCategories'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

import requests
import httplib2
import json
import random
import string

from flask import Flask, render_template, url_for, request, redirect
from flask import flash, jsonify, session as login_session, make_response
from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

app = Flask(__name__)

engine = create_engine('sqlite:///categoryitem.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"

## Check if google sign in works
## Add in fb login

# Login page
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Login through google account
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validates state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade authorization code to credential objects
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps
                                 ('Failed to upgrade authorization code'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check if access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # Aborts if there is an error
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that access token is valid for this app
    gplus_id = credentials.id_token['sub']
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does \
                                not match app's"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already \
                                connected'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session to use later
    login_session['provider'] = 'google'
    login_session['access_token'] = credentials.access_token
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(data['email'])
    if not user_id:
        user_id = createUser(login_session)

    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, ' + login_session['username']
    output += str(login_session['user_id'])
    output += '!</h1>'
    output += '<img src="' + login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: \
              150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output


# Create new user
def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# Gather user's info
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# Get the user's ID
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Disconnect from google account
@app.route('/gdisconnect')
def gdisconnect():
    # Disconnects the connected user
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps('Current user not connect'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_tokenn = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != 200:
        # If the given token was invalid
        response = make_response(json.dumps('Failed to revoke for given user'),
                                 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# Logout
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session == 'google':
            gdisonnect()
            del login_session['gplus_id']
            del login_session['credentials']
        del login_sesion['user_id']
        del login_sesion['username']
        del login_sesion['email']
        del login_sesion['picture']
        del login_sesion['provider']
        flash('You have been successfully logged out.')
        return redirect(url_for('showCategories'))
    else:
        flash('You were not logged in.')
        return redirect(url_for('showCategories'))


# Home page
@app.route('/')
@app.route('/categories')
def showCategories():
    categories = session.query(Category).all()
    lasttenitems = session.query(Item).order_by(Item.id.desc()).limit(10)
    return render_template('categories.html', categories=categories,
                           lasttenitems=lasttenitems)


# JSON of homepage with all the categories
@app.route('/categories/JSON')
def showCategoriesJSON():
    categories = session.query(Category).all()
    return jsonify(Categories=[c.serialize for c in categories])


# Shows the items in the category
@app.route('/category/<string:category_name>/')
@app.route('/category/<string:category_name>/items')
def showItemsInCategory(category_name):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    count = session.query(Item).filter_by(category_id=category.id).count()

    # If the user is not logged in, they can see the public version of page
    if 'username' not in login_session:
        return render_template('publiccategoryitems.html', category=category,
                               categories=categories, items=items,
                               count=count)
    else:
        return render_template('categoryitems.html', category=category,
                               categories=categories, items=items,
                               count=count)


# JSON of homepage with all the items in the category
@app.route('/category/<string:category_name>/JSON')
@app.route('/category/<string:category_name>/items/JSON')
def showItemsInCategoryJSON(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    return jsonify(Items=[i.serialize for i in items])


# Item page
@app.route('/category/<string:category_name>/<string:item_name>')
def showItem(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    c = session.query(Item).filter_by(category=category)
    item = c.filter_by(name=item_name).one()
    creator = getUserInfo(item.user_id)
    user_id = login_session['user_id']

    # If the user is not logged in, they can see the public version of page
    if 'username' not in login_session or creator.id != user_id:
        return render_template('publicitem.html', category=category, item=item,
                               creator=creator)
    else:
        return render_template('item.html', category=category, item=item,
                               creator=creator)


# JSON of the current item
@app.route('/category/<string:category_name>/<string:item_name>/JSON')
def showItemJSON(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    c = session.query(Item).filter_by(category=category)
    item = c.filter_by(name=item_name).one()
    return jsonify(Item=[item.serialize])


# Add new item to the current category
@app.route('/category/<string:category_name>/new', methods=['GET', 'POST'])
def newItem(category_name):
    # Redirects to login page if user is not logged in
    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name=category_name).one()
    if request.method == 'POST':
        newItem = Item(
            name=request.form['name'],
            description=request.form['description'],
            category=category, user_id=login_session['user_id'])
        # Prevents from adding a duplicate item into the same category
        c = session.query(Item).filter_by(category=category)
        count = c.filter_by(name=newItem.name).count()
        if count > 0:
            flash("Item already exists")
            return redirect(url_for('newItem', category_name=category_name,
                                    categories=categories))
        else:
            session.add(newItem)
            session.commit()
            flash("New item created")
        return redirect(url_for('showItemsInCategory',
                                category_name=category_name))
    else:
        return render_template('newitem.html', category_name=category_name,
                               categories=categories)


# Edit current item's info
@app.route('/category/<string:category_name>/<string:item_name>/edit',
           methods=['GET', 'POST'])
def editItem(category_name, item_name):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name=category_name).one()
    c = session.query(Item).filter_by(category=category)
    itemToEdit = c.filter_by(name=item_name).one()
    # Redirect user if not logged in
    if 'username' not in login_session:
        return redirect('/login')
    # Alerts users that they don't have permission to edit restaurant
    # if they aren't the creator
    if itemToEdit.user_id != login_session['user_id']:
        return "<script>function dontHavePermission() {alert('You are not \
        authorized to edit this item. Please create your own.');}\
        </script><body onload='dontHavePermission()'>"
    if request.method == 'POST':
        if request.form['name']:
            # Prevent duplicate items in same category
            c = session.query(Item).filter_by(category=category)
            count = c.filter_by(name=itemToEdit.name).count()
            if count > 0:
                flash("Item already exists")
                return redirect(url_for('editItem',
                                        category_name=category_name,
                                        item_name=item_name,
                                        categories=categories))
            else:
                itemToEdit.name = request.form['name']
        # Edit description
        if request.form['description']:
                itemToEdit.description = request.form['description']
        # Reassign category
        if request.form['category']:
            c = session.query(Category)
            newCategory = c.filter_by(name=request.form['category']).one()
            itemToEdit.category = newCategory
            itemToEdit.category_id = newCategory.id
        session.add(itemToEdit)
        session.commit()
        flash("Item successfully edited")
        return redirect(url_for('showItemsInCategory',
                                category_name=category_name))
    else:
        return render_template('edititem.html',
                               category_name=category_name,
                               item_name=item_name, item=itemToEdit,
                               categories=categories)


# Delete current item
@app.route('/category/<string:category_name>/<string:item_name>/delete',
           methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    c = session.query(Item).filter_by(category=category)
    itemToDelete = c.filter_by(name=item_name).one()
    # Redirect user if not logged in
    if 'username' not in login_session:
        return redirect('/login')
    # Alerts users that they don't have permission to delete restaurant
    # if they aren't the creator
    if itemToDelete.user_id != login_session['user_id']:
        return "<script>function dontHavePermission() {alert(\
        'You are not authorized to delete this item. Please create your own.'\
        );}</script><body onload='dontHavePermission()'>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Item successfully deleted")
        return redirect(url_for('showItemsInCategory',
                                category_name=category_name))
    else:
        return render_template('deleteitem.html',
                               category_name=category_name,
                               item_name=item_name)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

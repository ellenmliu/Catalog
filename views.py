from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

app = Flask(__name__)

engine = create_engine('sqlite:///categoryitem.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/categories')
def showCategories():
  categories = session.query(Category).all()
  return render_template('categories.html', categories = categories)

@app.route('/categories/JSON')
def showCategoriesJSON():
  categories = session.query(Category).all()
  return jsonify(Categories = [c.serialize for c in categories])

@app.route('/category/new', methods = ['GET', 'POST'])
def newCategory():
  if request.method == 'POST':
    newCategory = Category(
      name = request.form['name'])
    session.add(newCategory)
    session.commit()
    flash("New category created")
    return redirect(url_for('showCategories'))
  else:
    return render_template('newcategory.html')

@app.route('/category/<string:category_name>/edit', methods = ['GET', 'POST'])
def editCategory(category_name):
  categoryToEdit = session.query(Category).filter_by(name = category_name).one()
  if request.method == 'POST':
    if request.form['name']:
      categoryToEdit.name = request.form['name']
      session.add(categoryToEdit)
      session.commit()
      flash("Category successfully edited")
    return redirect(url_for('showCategories'))
  else:
    return render_template('editcategory.html', category_name = category_name, category = categoryToEdit)

@app.route('/category/<string:category_name>/delete', methods = ['GET', 'POST'])
def deleteCategory(category_name):
  categoryToDelete = session.query(Category).filter_by(name = category_name).one()
  if request.method == 'POST':
    session.delete(categoryToDelete)
    session.commit()
    flash("Category successfully deleted")
    return redirect(url_for('showCategories'))
  else:
    return render_template('deletecategory.html', category_name = category_name, category = categoryToDelete)

@app.route('/category/<string:category_name>/')
def showItemsInCategory(category_name):
  return ""

@app.route('/category/<string:category_name>/JSON')
def showItemsInCategoryJSON(category_name):
  return ""

@app.route('/category/<string:category_name>/<string:item_name>')
def showItem(category_name, item_name):
  return ""

@app.route('/category/<string:category_name>/<string:item_name>/JSON')
def showItemJSON(category_name, item_name):
  return ""

@app.route('/category/<string:category_name>/new', methods = ['GET', 'POST'])
def newItem(category_name):
  if request.method == 'POST':
    return ""
  else:
    return ""

@app.route('/category/<string:category_name>/<string:item_name>/edit', methods = ['GET', 'POST'])
def editItem(category_name, item_name):
  if request.method == 'POST':
    return ""
  else:
    return ""

@app.route('/category/<string:category_name>/<string:item_name>/delete', methods = ['GET', 'POST'])
def deleteItem(category_name, item_name):
  if request.method == 'POST':
    return ""
  else:
    return ""



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8080)

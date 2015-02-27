from app.mod_auth.controllers import mod_auth
from flask import Flask, Blueprint, render_template, redirect, url_for, request, flash, jsonify

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from database_setup import Base, Color
# Import module models (i.e. User)
from app.mod_color.models import Base, Color

from app import db

#engine = create_engine('sqlite:///colormenu.db')
#Base.metadata.bind = engine

#DBSession = sessionmaker(bind=engine)

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_color = Blueprint('color', __name__, url_prefix='/color')

@mod_color.route('/<int:color_id>/menu/JSON')
def colorMenuJSON(color_id):
    color = db.session.query(Color).filter_by(id=color_id).one()
    #items = session.query(MenuItem).filter_by(color_id=color_id).all()
    #return jsonify(MenuItems=[i.serialize for i in items])


@mod_color.route('/', methods=['GET'])
def colors():
    colors = Color.query.all()
    return render_template('color/colors.html', colors=colors)

# Task 1: Create route for newMenuItem function here
@mod_color.route('/new/', methods=['GET', 'POST'])
def new():
#    DBSession = sessionmaker(bind=db)
#    session = DBSession()
    if request.method == 'POST':
        new_color = Color(name=request.form['name'])
        db.session.add(new_color)
        db.session.commit()
        flash("new color created")
        return redirect(url_for('color.colors', color_id=new_color.id))
    else:
        return render_template('color/newcolor.html')

# Task 1: Create route for editMenuItem function here
@mod_color.route('/<int:color_id>/edit', methods=['GET', 'POST'])
def edit(color_id):
    editedColor = db.session.query(Color).filter_by(id=color_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedColor.name = request.form['name']
        db.session.add(editedColor)
        db.session.commit()
        flash("color edited")
        return redirect(url_for('color.colors'))
    else:
        return render_template('color/editcolor.html', color=editedColor)

@mod_color.route('/<int:color_id>/delete', methods=['GET', 'POST'])
def delete(color_id):
    colorToDelete = db.session.query(Color).filter_by(id=color_id).one()
    if request.method == 'POST':
        db.session.delete(colorToDelete)
        db.session.commit()
        flash("color deleted")
        return redirect(url_for('color.colors'))
    else:
        return render_template('color/deletecolor.html', color=colorToDelete)



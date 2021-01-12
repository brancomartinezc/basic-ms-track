from flask import render_template, url_for, redirect, request, flash, Blueprint
from flaskapp import db
from flaskapp.watched.forms import AddWatchedForm, EditWatchedForm
from flaskapp.models import User, Watched
from flask_login import current_user, login_required

watched = Blueprint('watched', __name__)


@watched.route('/add_watched', methods=['GET','POST'])
@login_required
def add_watched():
    form = AddWatchedForm()
    if form.validate_on_submit():
        new_watched = Watched(category=form.category.data, name=form.name.data, year=form.year.data, 
                        stars=form.stars.data, date=form.date.data, user=current_user)
        db.session.add(new_watched)
        db.session.commit()
        return redirect(url_for('watched._watched'))
    return render_template('watched/add_watched.html', form=form)

@watched.route('/watched')
@login_required
def _watched():
    watched = Watched.query.filter_by(user=current_user)
    return render_template('watched/watched.html', watched=watched)

@watched.route('/delete_watched/<id>')
@login_required
def delete_watched(id):
    #check that the current user is the owner of the row
    to_del_watched = Watched.query.filter_by(id=int(id)).first()
    if(to_del_watched.user_id == current_user.id):
        Watched.query.filter_by(id=int(id)).delete()
        db.session.commit()
        flash('The movie/series has been deleted.', 'success')
        return redirect(url_for('watched._watched'))
    return redirect(url_for('watched._watched'))

@watched.route('/edit_watched/<id>', methods=['GET','POST'])
@login_required
def edit_watched(id):
    #check that the current user is the owner of the row
    to_edit_watched = Watched.query.filter_by(id=int(id)).first()
    if(to_edit_watched.user_id == current_user.id):
        form = EditWatchedForm()
        if request.method == 'GET':
            form.category.data = to_edit_watched.category
            form.name.data = to_edit_watched.name
            form.year.data = to_edit_watched.year
            form.stars.data = to_edit_watched.stars
            form.date.data = to_edit_watched.date
        elif form.validate_on_submit():
            to_edit_watched.category = form.category.data
            to_edit_watched.name = form.name.data
            to_edit_watched.year = form.year.data
            to_edit_watched.stars = form.stars.data
            to_edit_watched.date = form.date.data
            flash('The movie/series has been updated.', 'success')
            db.session.commit()
            return redirect(url_for('watched._watched'))
        return render_template('watched/edit_watched.html', form=form )
    return redirect(url_for('watched._watched'))
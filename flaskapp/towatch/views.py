from flask import render_template, url_for, redirect, request, flash, Blueprint
from flaskapp import db
from flaskapp.towatch.forms import AddToWatchForm
from flaskapp.models import User, ToWatch
from flask_login import current_user, login_required

towatch = Blueprint('towatch', __name__)


@towatch.route('/add_towatch', methods=['GET','POST'])
@login_required
def add_towatch():
    form = AddToWatchForm()
    if form.validate_on_submit():
        new_towatch = ToWatch(category=form.category.data, name=form.name.data, user=current_user)
        db.session.add(new_towatch)
        db.session.commit()
        return redirect(url_for('towatch._towatch'))
    return render_template('towatch/add_towatch.html', form=form)

@towatch.route('/towatch')
@login_required
def _towatch():
    movies_towatch = ToWatch.query.filter_by(user=current_user, category='Movie')
    series_towatch = ToWatch.query.filter_by(user=current_user, category='Series')
    return render_template('towatch/towatch.html', movies_towatch=movies_towatch, series_towatch=series_towatch)

@towatch.route('/delete_towatch/<id>')
@login_required
def delete_towatch(id):
    #check that the current user is the owner of the row
    to_del_towatch = ToWatch.query.filter_by(id=int(id)).first()
    if(to_del_towatch.user_id == current_user.id):
        ToWatch.query.filter_by(id=int(id)).delete()
        db.session.commit()
        return redirect(url_for('towatch._towatch'))
    return redirect(url_for('towatch._towatch'))
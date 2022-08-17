from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Task
import json
from . import db


views = Blueprint('views', __name__)
@views.route('/', methods = ['GET', 'POST'])
@login_required 
def home():
    if request.method== "POST":
       task= request.form.get('task')
       if len(task)<1:
            flash ("task too short!", category = 'error')
       else:
           new_task = Task (data=task, user_id=current_user.id, finish=False)
           db.session.add(new_task)
           db.session.commit()
           flash('Task Added successfully :) ', category = 'success')
    
    return render_template('home.html', user=current_user)

@views.route('/delete-task', methods=["POST"])
def delete_task():
    task = json.loads(request.data)
    taskid = task['taskid']
    task = Task.query.get(taskid)
    if task:
        if task.user_id == current_user.id:
            db.session.delete(task)
            db.session.commit()
            flash('Task deleted successfully ', category = 'success')
    return jsonify({})


@views.route('/finish/<task_id>')
def finish_task(task_id):
    task_finished = Task.query.filter_by(id= task_id).first()
    if (task_finished.finish == True):
        task_finished.finish=False
    else:
        task_finished.finish=True
    db.session.commit()
    flash('Task completed successfully ', category = 'success')
    return redirect(url_for('views.home'))

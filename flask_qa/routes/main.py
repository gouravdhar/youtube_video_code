from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from flask_cors import CORS
from flask_qa.extensions import db
from flask_qa.models import Question, User, Stats, Notes
import json

main = Blueprint('main', __name__)

@main.route('/')
def index():
    questions = Question.query.filter(Question.answer != None).all()

    context = {
        'questions' : questions
    }

    return render_template('home.html', **context)

@main.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    if request.method == 'POST':
        question = request.form['question']
        expert = request.form['expert']

        question = Question(
            question=question, 
            expert_id=expert, 
            asked_by_id=current_user.id
        )

        db.session.add(question)
        db.session.commit()

        return redirect(url_for('main.index'))

    experts = User.query.filter_by(expert=True).all()

    context = {
        'experts' : experts
    }

    return render_template('ask.html', **context)

@main.route('/api', methods=['POST'])
def apiToPostStats():
    if request.method == 'POST':
        ip = request.form["ip"]
        loc = request.form["loc"]
        city = request.form["city"]
        country = request.form["country"]
        org = request.form["org"]
        postal = request.form["postal"]
        region = request.form["region"]
        timezone = request.form["timezone"]
        time = request.form["time"]

        stats = Stats(
            ip = ip,
            loc = loc,
            city = city,
            country = country,
            org = org,
            postal = postal,
            region = region,
            timezone = timezone,
            time = time
        )

        db.session.add(stats)
        db.session.commit()

        return "okay", 200


    return render_template('ask.html', **context)

@main.route('/api/postNotes', methods=['POST', 'GET'])
def apiToPostNotes():
    if request.method == 'POST':
        # id = request.form["id"]
        userName = request.form["username"]
        notesEntry = request.form["notes"]

        notesRow = Notes.query.filter_by(username=userName).first()
        if not notesRow:
            notes=Notes(
                notes=notesEntry,
                username=userName
            )
            db.session.add(notes)
            db.session.commit()
        else:
            idRow=notesRow.id
            notes = Notes(
                id=idRow,
                notes=notesEntry,
                username=userName
            )
            db.session.add(notes)
            db.session.commit()
        # if not notesRow:
        #     notes = Notes(
        #         notes = notesEntry,
        #         username = username
        #     )

        #     db.session.add(notes)
        #     db.session.commit()
        # else:
        #     id = notesRow.id
        #     notes = Notes(
        #         id=id;
        #         notes = notesEntry,
        #         username = username
        #     )

        #     db.session.add(notes)
        #     db.session.commit()
        
        return "okay", 200


    return render_template('ask.html', **context)

@main.route('/api/getNotes/<userName>', methods=['GET'])
def apiToGetNotes(userName):
    if request.method == 'GET':
        notes = Notes.query.filter_by(username=userName).first()
        if not notes:
            return "not okay", 200
        return json.dumps(notes.notes), 200


    return 'hi',200

@main.route('/api/coord', methods=['GET'])
def apiToGetCoords():
    if request.method == 'GET':
        stats = Stats.query.filter().all()
        coords = []
        for stat in stats:
            coordinate = []
            first = float(stat.loc.split(',')[0])
            second = float(stat.loc.split(',')[1])
            coordinate.append(second)
            coordinate.append(first)
            coords.append(coordinate)
        
        return json.dumps(coords), 200


    return 'hi',200

@main.route('/api/get-records/awersgfjkweshjbs', methods=['GET'])
def apiToGetStats():
    if request.method == 'GET':
        stats = Stats.query.filter().all()
        coords = []
        for stat in stats:
            row1= []
            row1.append(stat.ip)
            row1.append(stat.loc)
            row1.append(stat.city)
            row1.append(stat.country)
            row1.append(stat.org)
            row1.append(stat.postal)
            row1.append(stat.region)
            row1.append(stat.timezone)
            row1.append(stat.time)
            # row=stat.ip+','+stat.loc+','+stat.city+','+stat.country+','+stat.org+','+stat.postal+','+stat.region+','+stat.timezone+','+stat.time
            coords.append(row1)
        
        return json.dumps(coords), 200


    return 'hi',200

@main.route('/answer/<int:question_id>', methods=['GET', 'POST'])
@login_required
def answer(question_id):
    if not current_user.expert:
        return redirect(url_for('main.index'))

    question = Question.query.get_or_404(question_id)

    if request.method == 'POST':
        question.answer = request.form['answer']
        db.session.commit()

        return redirect(url_for('main.unanswered'))

    context = {
        'question' : question
    }

    return render_template('answer.html', **context)

@main.route('/question/<int:question_id>')
def question(question_id):
    question = Question.query.get_or_404(question_id)

    context = {
        'question' : question
    }

    return render_template('question.html', **context)

@main.route('/unanswered')
@login_required
def unanswered():
    if not current_user.expert:
        return redirect(url_for('main.index'))

    unanswered_questions = Question.query\
        .filter_by(expert_id=current_user.id)\
        .filter(Question.answer == None)\
        .all()

    context = {
        'unanswered_questions' : unanswered_questions
    }

    return render_template('unanswered.html', **context)

@main.route('/users')
@login_required
def users():
    if not current_user.admin:
        return redirect(url_for('main.index'))

    users = User.query.filter_by(admin=False).all()

    context = {
        'users' : users
    }

    return render_template('users.html', **context)

@main.route('/promote/<int:user_id>')
@login_required
def promote(user_id):
    if not current_user.admin:
        return redirect(url_for('main.index'))

    user = User.query.get_or_404(user_id)

    user.expert = True
    db.session.commit()

    return redirect(url_for('main.users'))
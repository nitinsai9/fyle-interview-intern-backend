from flask import jsonify,abort
from marshmallow.exceptions import ValidationError
from core import app
from core.apis.assignments import student_assignments_resources , teacher_assignment

from core.libs import helpers
from core.libs.exceptions import FyleError
from werkzeug.exceptions import HTTPException

from sqlalchemy.exc import IntegrityError
from core import db

from core.models.assignments import Assignment 


app.register_blueprint(student_assignments_resources, url_prefix='/student')
app.register_blueprint(teacher_assignment , url_prefix = '/teacher')


@app.route('/')
def ready():
    response = jsonify({
        'status': 'ready',
        'time': helpers.get_utc_now()
    })

    return response
''' This is for rolling back the change made during testing is real case we can remove this . Just for the test case to run I have used this '''

@app.route('/rollback' , methods=['GET'] , strict_slashes=False)
def clearup():
    Assignment.rollback_assignment_2(2)
    db.session.commit()
    response =  jsonify({ 'Done' : 'Updated'})
    if response is None:
        abort(404, description="Resource not found")
    
    return response 



@app.errorhandler(Exception)
def handle_error(err):
    if isinstance(err, FyleError):
        return jsonify(
            error=err.__class__.__name__, message=err.message
        ), err.status_code
    elif isinstance(err, ValidationError):
        return jsonify(
            error=err.__class__.__name__, message=err.messages
        ), 400
    elif isinstance(err, IntegrityError):
        return jsonify(
            error=err.__class__.__name__, message=str(err.orig)
        ), 400
    elif isinstance(err, HTTPException):
        return jsonify(
            error=err.__class__.__name__, message=str(err)
        ), err.code

    raise err

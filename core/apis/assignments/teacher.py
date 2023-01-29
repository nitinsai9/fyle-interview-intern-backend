from flask import Blueprint 
from core import db 
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from .schema import AssignmentSchema, teacher_payload



teacher_assignment= Blueprint('teacher_assignment', __name__)



@teacher_assignment.route('/assignments' , methods=['GET'], strict_slashes=False) 
@decorators.auth_principal 
def list_assignments_teacher(p):
    """return all the assignments submited to the teacher """
    assignment = Assignment.get_assignment_by_teacher(p.teacher_id)
    teacher_assignments_dump = AssignmentSchema().dump(assignment, many=True)
    return APIResponse.respond(data=teacher_assignments_dump)



@teacher_assignment.route('/assignments/grade' , methods = ['POST'] , strict_slashes= False)
@decorators.accept_payload
@decorators.auth_principal
def update_grade(p,incoming_payload):
    """ grade an assignment """
    
    grade_payload = teacher_payload().load(incoming_payload)
    
    grade_submit = Assignment.grade_assignment( _id = grade_payload.id , grade = grade_payload.grade,principal= p )

    db.session.commit()
    grade_submit_dump = AssignmentSchema().dump(grade_submit)
    return APIResponse.respond(data = grade_submit_dump)

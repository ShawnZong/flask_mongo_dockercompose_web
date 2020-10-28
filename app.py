
from flask import Flask, jsonify, request, Response
from database.db import initialize_db
from database.models import Professor, ResearchGroup, Student
import json
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# database configs
app.config['MONGODB_SETTINGS'] = {
    # set the correct parameters here as required, some examples aer give below
    'host': 'mongodb://mongo:27017/flask-db'
    # 'host': 'mongodb://localhost/flaskdb'
}
db = initialize_db(app)

# Root


@app.route('/')
def get_route():
    output = {
        'message': 'It looks like you are trying to access FlaskAPP over HTTP on the native driver port.'}
    return output, 200

# Update the methods below


@app.route('/listProfessor', methods=['POST'])
def add_professor():
    # add professor worked-----------
    body = request.get_json()
    professor = Professor(**body).save()
    response = {'message': 'Professor successfully created',
                'id': str(professor.id)}
    return response, 201


@app.route('/listProfessor/<prof_id>', methods=['GET'])
def get_professor_by_id(prof_id):
    # get professo by id wored-------------
    professor = Professor.objects.get_or_404(id=prof_id)

    response = {'name': str(professor.name), 'email': str(professor.email),
                'designation': str(professor.designation), 'interests': professor.interests}
    return response, 200


@app.route('/listProfessors', methods=['GET'])
def get_professor_by_designation_or_groupname():
    designation = request.args.get('designation')
    groupname = request.args.get('groupName')
    if designation:
        # get professor by designation worked----------
        professor_list = Professor.objects(designation=designation)
        if professor_list:
            response = [{'name': professor.name, 'email': professor.email}
                        for professor in professor_list]
            response = jsonify(response)
            return response, 200
        else:
            response = {'message': 'Not Found'}
            return response, 404

    elif groupname:
        # get professors by groupname worked--------------
        group = ResearchGroup.objects.get(name=groupname)
        professor_list = Professor.objects(researchGroups=group)
        if professor_list:
            response = [{'name': professor.name, 'email': professor.email}
                        for professor in professor_list]
            response = jsonify(response)
            return response, 200
        else:
            response = {'message': 'Not Found'}
            return response, 404


@app.route('/listProfessor/<prof_id>', methods=['PUT'])
def update_prof(prof_id):
    # update professor worked---------
    body = request.get_json()
    if body:
        # Update Code here
        researchgroup_ids = [ObjectId(tmp) for tmp in body['researchGroups']]

        body['researchGroups'] = researchgroup_ids
        Professor.objects.get(id=prof_id).update(**body)
        response = {'message': 'Professor successfully updated',
                    'id': str(prof_id)}
        return response, 200
    else:
        # Update Code here
        response = {'message': 'No Content'}
        return response, 204


@app.route('/listProfessor/<prof_id>', methods=['DELETE'])
def delete_professor_by_id(prof_id):
    # delete professor worked----------
    professor = Professor.objects.get(id=prof_id).delete()
    response = {"message": "Professor successfully deleted",
                "id": str(prof_id)}
    return response, 200


@app.route('/listGroup', methods=['POST'])
def add_researchgroup():
    # add researchgroup worked--------------
    body = request.get_json()
    researchgroup = ResearchGroup(**body).save()

    if researchgroup:
        response = {'message': 'Group successfully created',
                    'id': str(researchgroup.id)}
        return response, 201
    else:
        response = {'message': 'Conflict'}
        return response, 409


@app.route('/listGroup/<group_id>', methods=['GET', 'PUT', 'DELETE'])
def rud_group(group_id):
    if request.method == 'GET':
        # get researchgroup worked--------------
        researchgroup = ResearchGroup.objects.get(id=group_id)
        if researchgroup:
            response = {'id': str(group_id), 'name': str(
                researchgroup.name), 'founder': str(researchgroup.founder.id)}
            return response, 200
        else:
            response = {'message': 'Not Found'}
            return response, 404
    elif request.method == 'PUT':
        # update researchgroup worked--------------
        body = request.get_json()
        if body:
            body['founder'] = ObjectId(body['founder'])
            ResearchGroup.objects.get(id=group_id).update(**body)
            response = {'message': 'Group successfully updated',
                        'id': str(group_id)}
            return response, 200
        else:
            response = {'message': 'No Content'}
            return response, 204
    elif request.method == 'DELETE':
        # delete researchgroup worked----------
        ResearchGroup.objects.get_or_404(id=group_id).delete()
        response = {'message': 'Group successfully deleted',
                    'id': str(group_id)}
        return response, 200


@app.route('/listStudent/<student_id>', methods=['GET', 'PUT', 'DELETE'])
def get_student_by_id(student_id):
    """
    Get (read), update or delete a student

    Args:
        student_id (Object id): The student Id of the student record that nees to be modified.

    Returns:
        dict: The dictionary with output values
        int : The status code
    """

    if request.method == 'GET':
        # get studeny by id worked---------------

        student = Student.objects.get(id=student_id)
        if student:
            # Update Code here
            researchgroup_ids = [str(tmp.id)
                                 for tmp in student.researchGroups]
            response = {'name': str(student.name), 'studentNumber': str(student.studentNumber),
                        'researchGroups': researchgroup_ids}
            response = jsonify(response)
            return response, 200
            # output = {'name': "", 'studentNumber': "", 'researchGroups': ""}
        else:
            # Update Code here
            response = {'message': 'Not Found'}
            return response, 404
    elif request.method == 'PUT':
        # put worked-----------------------
        body = request.get_json()
        if body:
            # Update Code here
            if 'researchGroups' in body:
                researchgroup_ids = [ObjectId(tmp)
                                     for tmp in body['researchGroups']]
                body['researchGroups'] = researchgroup_ids

            Student.objects(id=student_id).update(**body)
            response = {'message': 'Student successfully updated',
                        'id': str(student_id)}
            return response, 200
        else:
            # Update Code here
            response = {'message': 'No Content'}
            return response, 204
    elif request.method == 'DELETE':
        # delete worked-----------------
        Student.objects.get_or_404(id=student_id).delete()
        response = {'message': 'Student successfully deleted',
                    'id': str(student_id)}
        return response, 200


@app.route('/listStudents', methods=['GET'])
def get_student_by_groupname():
    # get students by groupname worked-----------
    groupname = request.args.get('groupName')
    if groupname:
        group = ResearchGroup.objects.get(name=groupname)
        student_list = Student.objects(researchGroups=group)
        response = [{'name': student.name, 'studentNumber': student.studentNumber}
                    for student in student_list]

        response = jsonify(response)
        return response, 200

    else:
        response = {'message': 'Not Found'}
        return response, 404
    # Complete the  request methods below


@app.route('/listStudent', methods=['POST'])
# worked---------------------------
def add_student():
    """
    This function creates a new student given student_id in the request body

    Returns:
        dict: Dictionary containing the message and id
        int : The status code
    """

    # Update the code here.
    body = request.get_json()
    student = Student(**body).save()

    if student:
        response = {'message': 'Student successfully created',
                    'id': str(student.id)}
        return response, 201
    else:
        response = {'message': 'Conflict'}
        return response, 409


# Only for local testing without docker
# app.run()  # FLASK_APP=app.py FLASK_ENV=development flask run

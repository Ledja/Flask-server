from os import abort
from ..services import  PersonService
from flask import request, Blueprint, jsonify, make_response

person = Blueprint('person', __name__)

     

@person.route("/person/", methods=['POST'])
def create_person():
    post_data       = eval(request.data)
    incoming_age    = post_data['age']
    incoming_name   = post_data['name']

    if type(incoming_age) is not int :
        return make_response(jsonify( {'age': ['Not a valid integer']}), 400)
        
    if int(incoming_age)>100:
        return make_response(jsonify({'age': ['Person too old. Max age is 100']}), 400)
    
    
    res = PersonService().create_person_api(name=incoming_name,age=incoming_age)
    return make_response(jsonify(res),201)
    

@person.route("/person/<int:id>", methods=['GET'])
def get_person_by_id(id):    
    all_ids = PersonService().get_all_available_ids_api()
    if id in all_ids:
        res = PersonService().get_person_by_id_api(id)
        return make_response(jsonify(res), 200)
    else: 
        return make_response("Not Found!", 404)
     



        





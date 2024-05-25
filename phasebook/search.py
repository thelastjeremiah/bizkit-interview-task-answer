from flask import Blueprint, request, Response
import json

from .data.search_data import USERS

bp = Blueprint("search", __name__, url_prefix="/search")

@bp.route("")
def search():
    users = search_users(request.args.to_dict())
    response_data = [reorder_user_fields(user) for user in users]
    response_data.sort(key=lambda user: int(user['id']))
    return Response(json.dumps(response_data, indent=2), mimetype='application/json')

def search_users(args):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters
    """
    
    if not args:
        return USERS

    result = []
    matched_ids = set()

    if 'id' in args:
        user_id = args['id']
        for user in USERS:
            if user['id'] == user_id:
                result.append(user)
                matched_ids.add(user['id'])
                break

    for user in USERS:
        if user['id'] in matched_ids:
            continue

        match = False
                
        if 'name' in args and args['name'].lower() in user['name'].lower():
            match = True

        if 'age' in args:
            target_age = int(args['age'])
            if target_age - 1 <= user['age'] <= target_age + 1:
                match = True
                
        if 'occupation' in args and args['occupation'].lower() in user['occupation'].lower():
            match = True

        if match:
            result.append(user)
            matched_ids.add(user['id'])

    return result

def reorder_user_fields(user):
    return {
        "id": user["id"],
        "name": user["name"],
        "age": user["age"],
        "occupation": user["occupation"]
    }

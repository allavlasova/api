__author__ = 'alla'
from flask import request
from flask import Blueprint
from db import get_db
from pymysql import DatabaseError
from  function import *
from response import *
from post_queries import *

post = Blueprint('post', __name__)
BASE_URL = "/post"


@post.route(BASE_URL + '/details/')
def datails():
    id = int(request.args.get('post'))
    if id == None or id < 0:
        return response_1
    cursor = get_db().cursor()
    related = request.args.getlist('related')
    for i in related:
        if i not in ['user', 'thread', 'forum']:
            cursor.close()
            return response_3
    response = make_response_for_post(id, cursor, related)
    if response == None:
        cursor.close()
        return response_1
    return make_response(0, response)

@post.route(BASE_URL + '/create/', methods=['POST'])
def create():
    db = get_db()
    cursor = db.cursor()
    try:
        data = ujson.loads(request.data)
    except ValueError:
        cursor.close()
        return response_2
    try:
       date = data['date']
       thread = data['thread']
       message = data['message']
       user = data['user']
       forum = data['forum']
    except (KeyError):
        cursor.close()
        return response_2
    parametr = []
    parametr.append(date)
    parametr.append(thread)
    parametr.append(message)
    parametr.append(user)
    parametr.append(forum)
    try:
        parent = data['parent']
        if(parent != None):
            if(cursor.execute(get_post_id, [parent]) == 0):
                cursor.close()
                return response_1
    except KeyError:
        parent = None
    try:
        isApproved = data['isApproved']
    except KeyError:
        isApproved = False
    try:
        isHighlighted = data['isHighlighted']
    except KeyError:
        isHighlighted = False
    try:
        isEdited = data['isEdited']
    except KeyError:
        isEdited = False
    try:
        isSpam = data['isSpam']
    except KeyError:
        isSpam = False
    try:
        isDeleted = data['isDeleted']
    except KeyError:
        isDeleted = False
    parametr.append(parent)
    parametr.append(isApproved)
    parametr.append(isHighlighted)
    parametr.append(isEdited)
    parametr.append(isSpam)
    parametr.append(isDeleted)
    try:
        cursor.execute(create_post, parametr)
        id_post = cursor.lastrowid
        db.commit()
    except DatabaseError:
        return response_5
    data = []
    data.extend([id_post, date, message, isApproved, isDeleted, isEdited, isHighlighted, isSpam, 0, 0, 0, thread, parent])
    response = Post_reaponse(data, user, forum, thread)
    return make_response(0, response)


@post.route(BASE_URL + '/list/')
def list():
    cursor = get_db().cursor()
    forum = request.args.get('forum')
    thread = request.args.get('thread')
    since = Optional_sience_date(request)
    add_order = Optional_order(request)
    add_limit = optional_Limit(request)
    if forum != None:
        get_list_post_id = get_list_post_data_by_forum
        param = forum
    else:
        param = thread
        get_list_post_id = get_list_post_data_by_thread
    try:
        cursor.execute(get_list_post_id + since + add_order + add_limit,[param])
    except (DatabaseError):
        cursor.close()
        return response_4
    post_list = []
    for data in cursor.fetchall():
        res = {
        "id" : data[0],
        "date":str(data[1]),
        "message": data[2],
        "isApproved" : data[3],
        "isDeleted" : data[4],
        "isEdited" : data[5],
        "isHighlighted": data[6],
        "isSpam" : data[7],
        "dislikes": data[8],
        "likes": data[9],
        "points": data[9] - data[8],
        "thread": data[10],
        "parent": data[11],
        "user" : data[12],
        "forum" : data[13]
        }
        post_list.append(res)
    return make_response(0, post_list)


@post.route(BASE_URL + '/remove/', methods=['POST'])
def remove():
    try:
        data = ujson.loads(request.data)
    except ValueError:
        return response_2
    try:
       post_id = data['post']
    except (KeyError):
        return response_2
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(remove_post,[post_id])
        db.commit()
    except DatabaseError:
        cursor.close()
        return response_4
    cursor.close()
    return make_response(0, {"post": post_id})

@post.route(BASE_URL + '/restore/', methods=['POST'])
def restore():
    try:
        data = ujson.loads(request.data)
    except ValueError:
        return response_2
    try:
       post_id = data['post']
    except (KeyError):
        return response_2
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(restore_post,[post_id])
        db.commit()
    except DatabaseError:
        cursor.close()
        return response_4
    cursor.close()
    return make_response(0, {"post": post_id})


@post.route(BASE_URL + '/update/', methods=['GET', 'POST'])
def update():
    if(request.method == 'GET'):
        return response_2
    db = get_db()
    cursor = db.cursor()
    try:
        data = ujson.loads(request.data)
    except ValueError:
        cursor.close()
        return response_2
    try:
       post_id = data['post']
       message = data['message']
    except (KeyError):
        cursor.close()
        return response_2
    try:
        cursor.execute(update_post,[message, post_id])
        db.commit()
    except DatabaseError:
        cursor.close()
        return response_4
    response = make_response_for_post(post_id, cursor,[])
    cursor.close()
    return make_response(0, response)

@post.route(BASE_URL + '/vote/', methods=['POST'])
def vote():
    db = get_db()
    cursor = db.cursor()
    try:
        data = request.get_json()
    except ValueError:
        cursor.close()
        return response_2
    try:
       post_id = data['post']
       vote = data['vote']
    except (KeyError):
        cursor.close()
        return response_2
    if vote == 1:
        query = get_like
    elif vote == -1:
        query = get_dislike
    else:
        cursor.close()
        return response_2
    try:
        cursor.execute(query, [post_id])
        db.commit()
    except DatabaseError:
        cursor.close()
        return response_4
    response = make_response_for_post(post_id, cursor, [])
    return make_response(0, response)
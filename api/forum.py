__author__ = 'alla'
from flask import request
from flask import Blueprint
from db import get_db
from pymysql import DatabaseError
from  function import *
from response import *
forum = Blueprint('forum', __name__)
BASE_URL = "/forum"
from forum_queries import create_forum, list_data_post, data_thread_by_forum_short_name, user_list

@forum.route(BASE_URL + '/create/', methods=['POST'])
def create():
    try:
        db = get_db()
    except DatabaseError:
        return response_4
    cursor = db.cursor()
    try:
        data = request.get_json()
    except ValueError:
        cursor.close()
        return response_2
    try:
       name = data['name']
       short_name = data['short_name']
       user = data['user']
    except (KeyError):
        cursor.close()
        return response_2
    try:
        cursor.execute(create_forum, [name, short_name, user])
        db.commit()
    except DatabaseError:
        cursor.close()
        return response_4
    id = cursor.lastrowid
    data = []
    data.extend([id, name, short_name])
    response = Forum_response(data, user)
    cursor.close()
    return make_response(0, response)

@forum.route(BASE_URL + '/details/')
def datails():
    short_name = request.args.get('forum')
    if(short_name == None):
        return response_2
    cursor = get_db().cursor()
    related = request.args.get('related')
    response = make_response_for_forum_by_short_name(short_name, cursor, related)
    if response == None:
        cursor.close()
        return response_1
    cursor.close()
    return make_response(0, response)

@forum.route(BASE_URL + '/listPosts/')
def listPosts():
    short_name = request.args.get('forum')
    cursor = get_db().cursor()
    if(short_name == None):
        return response_2
    related_list = request.args.getlist('related')
    since = request.args.get('since')
    if since != None:
        since =  "AND Post.date>= '%s' " % since
    else:
        since =  ''
    add_order = Optional_order(request)
    add_limit = optional_Limit(request)
    try:
        cursor.execute(list_data_post + since + add_order + add_limit,[short_name])
    except DatabaseError:
        cursor.close()
        return response_4
    list_post = []
    posts = [i for i in cursor.fetchall()]
    if 'forum' in related_list:
        forum = make_response_for_forum_by_short_name(short_name, cursor, [])
    else:
        forum = short_name
    for post in posts:
        if 'user' in related_list:
            user = make_response_for_user_by_email(post[12], cursor)
        else:
            user = post[12]
        if 'thread' in related_list:
            thread = make_response_for_thread(post[10], cursor)
        else:
            thread = post[10]
        res =  {
        "id" : post[0],
        "date":str(post[1]),
        "message": post[2],
        "isApproved" : post[3],
        "isDeleted" : post[4],
        "isEdited" : post[5],
        "isHighlighted": post[6],
        "isSpam" : post[7],
        "dislikes": post[8],
        "likes": post[9],
        "points": post[9] - post[8],
        "thread": thread,
        "parent": post[11],
        "user" : user,
        "forum" : forum
    }
        list_post.append(res)
    cursor.close()
    return make_response(0, list_post)


@forum.route(BASE_URL + '/listUsers/')
def listUsers():
    short_name = request.args.get('forum')
    since = request.args.get('since_id')
    cursor = get_db().cursor()
    if since != None:
        since =  " AND user_id >= %s " % since
    else:
        since =  ''
    order = request.args.get('order')
    if order == None or order == 'desc':
        add_order  = ' ORDER BY user.name DESC'
    elif order == 'asc':
        add_order = ' ORDER BY user.name ASC'
    add_limit = optional_Limit(request)
    try:
        cursor.execute(user_list  + since + add_order + add_limit, [short_name])
    except DatabaseError:
        cursor.close()
        return response_4
    list_user = []
    for data in cursor.fetchall():
        followers = user_followers(data[5], cursor)
        following = user_following(data[5], cursor)
        subscriptions = user_subscriptions(data[5], cursor)
        response = {
                "about": data[2],
                "email": data[5],
                "followers": followers,
                "following": following,
                "id": data[4],
                "isAnonymous": data[3],
                "name": data[0],
                "subscriptions": subscriptions,
                "username": data[1]
            }
        list_user.append(response)
    return make_response(0, list_user)


@forum.route(BASE_URL + '/listThreads/')
def listThreads():
    short_name = request.args.get('forum')
    if(short_name == None):
        return response_2
    cursor = get_db().cursor()
    related_list = request.args.getlist('related')
    since = Optional_sience_date(request)
    add_order = Optional_order(request)
    add_limit = optional_Limit(request)
    try:
        cursor.execute(data_thread_by_forum_short_name + since + add_order + add_limit,[short_name])
    except DatabaseError:
        cursor.close()
        return response_4
    list_threads = []
    threads =  cursor.fetchall()
    if 'forum' in related_list:
        forum = make_response_for_forum_by_short_name(short_name, cursor, [])
    else:
        forum = short_name
    for data in threads:
        if 'user' in related_list:
            user = make_response_for_user_by_email(data[10], cursor)
        else:
            user = data[10]
        res  = {
        "id": data[0],
        "title": data[1],
        "isClosed": data[2],
        "date": str(data[3]),
        "message": data[4],
        "slug": data[5],
        "isDeleted": data[6],
        "likes": data[7],
        "dislikes": data[8],
        "forum": forum,
        "points": int(data[7]) - int(data[8]),
        "posts": data[9],
        "user": user
        }
        list_threads.append(res)
    return make_response(0, list_threads)





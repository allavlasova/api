__author__ = 'alla'
from flask import Flask, request
from pymysql import DatabaseError
from flask import Blueprint
from db import get_db
from  function import *
from response import *
from thread_queries import close_thread, create_thread, get_dislike_for_thread, get_like_for_thread, update_thread, get_unsubscribe, \
get_subscribe, restore_thread, restore_the_posts_in_the_thread, remove_the_posts_in_the_thread, remove_thread, open_thread, get_list_thread_data_by_forum_short_name, \
get_list_thread_data_by_user_email, list_data_post_by_thread_id, posts_by_thread_id_related_user_forum, posts_by_thread_id_related_user, posts_by_thread_id_related_forum


thread = Blueprint('thread', __name__)
BASE_URL = "/thread"

@thread.route(BASE_URL + '/details/')
def datails():
    id = request.args.get('thread')
    if id == None or int(id) < 0:
        return response_2
    related_list = request.args.getlist('related')
    for related in related_list:
        if related not in ['user', 'forum']:
            return response_3
    cursor = get_db().cursor()
    response = make_response_for_thread(id, cursor, related_list)
    if response == None:
        return response_1
    return make_response(0, response)


@thread.route(BASE_URL + '/close/', methods=['POST'])
def close():
    try:
        data = request.get_json()
    except ValueError:
        return response_2
    try:
       id = data['thread']
    except (KeyError):
        return response_2
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(close_thread,[id])
        db.commit()
    except DatabaseError:
        cursor.close()
        return response_4
    return make_response(0, {"thread": id})

@thread.route(BASE_URL + '/create/', methods=['GET', 'POST'])
def create():
    if(request.method == 'GET'):
        return make_response(2, response_2)
    db = get_db()
    cursor = db.cursor()
    data = request.get_json()
    try:
       forum = data['forum']
       title = data['title']
       isClosed = data['isClosed']
       user = data['user']
       date = data['date']
       message  = data['message']
       slug = data['slug']
    except (KeyError):
        cursor.close()
        return response_2
    try:
        isDeleted = data['isDeleted']
    except (KeyError):
        isDeleted = False
    try:
        cursor.execute(create_thread, [title, date, message, slug, user, forum, isClosed, isDeleted])
        id = cursor.lastrowid
        db.commit()
    except DatabaseError:
        return response_4
    response = {
        "id": id,
        "title": title,
        "isClosed": isClosed,
        "date": str(date),
        "message": message,
        "slug": slug,
        "isDeleted": isDeleted,
        "likes": 0,
        "dislikes": 0,
        "forum": forum,
        "points": 0,
        "posts": 0,
        "user": user
    }
    return make_response(0, response)




@thread.route(BASE_URL + '/list/')
def list():
    cursor = get_db().cursor()
    forum = request.args.get('forum')
    user = request.args.get('user')
    since = Optional_sience_date(request)
    add_order = Optional_order(request)
    add_limit = optional_Limit(request)
    if forum != None:
        get_list_id = get_list_thread_data_by_forum_short_name
        param = forum
    else:
        param = user
        get_list_id = get_list_thread_data_by_user_email
    try:
        cursor.execute(get_list_id + since + add_order + add_limit,[param])
    except (DatabaseError):
        cursor.close()
        return response_4
    list = []
    for data in cursor.fetchall():
        res =  {
        "id": data[0],
        "title": data[1],
        "isClosed": data[2],
        "date": str(data[3]),
        "message": data[4],
        "slug": data[5],
        "isDeleted": data[6],
        "likes": data[7],
        "dislikes": data[8],
        "forum": data[11],
        "points": int(data[7]) - int(data[8]),
        "posts": data[9],
        "user": data[10]
        }
        list.append(res)
    return make_response(0, list)


@thread.route(BASE_URL + '/listPosts/')
def listPosts():
    thread = request.args.get('thread')
    if(thread == None):
        return response_2
    cursor = get_db().cursor()
    related_list = request.args.getlist('related')
    since = Optional_sience_date(request)
    add_order = Optional_order(request)
    limit = request.args.get('limit')
    if limit != None:
        add_limit = ' LIMIT '+limit+";"
    else:
        add_limit = ";"
    if 'user' in related_list and 'forum' in related_list:
        try:
            cursor.execute(posts_by_thread_id_related_user_forum + since + add_order, [thread])
        except:
            cursor.close()
            response_4
    elif 'user' in related_list and 'forum' not in related_list:
        try:
            cursor.execute(posts_by_thread_id_related_user + since + add_order, [thread])
        except:
            cursor.close()
            response_4
    elif 'user' not in related_list and 'forum' in related_list:
        try:
            cursor.execute(posts_by_thread_id_related_forum + since + add_order, [thread])
        except:
            cursor.close()
            response_4
    else:
        try:
            cursor.execute(list_data_post_by_thread_id + since + add_order + add_limit,[thread])
        except (DatabaseError):
            cursor.close()
            return response_4
    list_post = []
    posts = cursor.fetchall()
    if 'thread' in related_list:
        thread = make_response_for_thread(int(thread), cursor)
    else:
        thread = int(thread)
    for data in posts:
        if 'user' in related_list and 'forum' in related_list:
            followers = user_followers(data[12], cursor)
            following = user_following(data[12], cursor)
            subscriptions = user_subscriptions(data[12], cursor)
            user  = {
                "about": data[16],
                "email": data[12],
                "followers": followers,
                "following": following,
                "id": data[18],
                "isAnonymous": data[17],
                "name": data[14],
                "subscriptions": subscriptions,
                "username": data[15]
                }
            forum =  {
                "id": data[21],
                "name": data[19],
                "short_name": data[13],
                "user": data[20]
                }
        elif 'user' in related_list and 'forum' not in related_list:
            user  = {
                "about": data[16],
                "email": data[12],
                "followers": followers,
                "following": following,
                "id": data[18],
                "isAnonymous": data[17],
                "name": data[14],
                "subscriptions": subscriptions,
                "username": data[15]
                }
            forum = data[13]
        elif 'user' not in related_list and 'forum' in related_list:
            user = data[12]
            forum = {
                "id": data[16],
                "name": data[14],
                "short_name": data[13],
                "user": data[15]
                }
        else:
            user = data[12]
            forum = data[13]
        res =  {
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
        "thread": thread,
        "parent": data[11],
        "user" : user,
        "forum" : forum
         }
        list_post.append(res)
    return make_response(0, list_post)



@thread.route(BASE_URL + '/open/', methods=['POST'])
def open():
    try:
        data = request.get_json()
    except ValueError:
        return response_2
    try:
       id = data['thread']
    except (KeyError):
        return response_2
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(open_thread,[id])
        db.commit()
    except DatabaseError:
        cursor.close()
        return response_4
    cursor.close()
    return make_response(0, {"thread": id})

@thread.route(BASE_URL + '/remove/', methods=['POST'])
def remove():
    try:
        data = request.get_json()
    except ValueError:
        return response_2
    try:
       id = data['thread']
    except (KeyError):
        return response_2
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(remove_thread,[id])
        cursor.execute(remove_the_posts_in_the_thread, [id])
        db.commit()
    except DatabaseError:
        cursor.close()
        return response_4
    cursor.close()
    return make_response(0, {"thread": id})


@thread.route(BASE_URL + '/restore/', methods=['POST'])
def restore():
    db = get_db()
    cursor = db.cursor()
    try:
        data = request.get_json()
    except ValueError:
        cursor.close()
        return response_2
    try:
       id = data['thread']
    except (KeyError):
        cursor.close()
        return response_2
    try:
        cursor.execute(restore_thread,[id])
        cursor.execute(restore_the_posts_in_the_thread, [id])
        db.commit()
    except DatabaseError:
        cursor.close()
        return response_4
    cursor.close()
    return make_response(0, {"thread": id})


@thread.route(BASE_URL + '/subscribe/', methods=['GET', 'POST'])
def subscribe():
    if(request.method == 'GET'):
        return response_2
    try:
        data = request.get_json()
    except ValueError:
        return response_2
    try:
       thread = data['thread']
       user = data['user']
    except (KeyError):
        return response_2
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(get_subscribe, [user, thread])
        db.commit()
    except DatabaseError:
        cursor.close()
        return response_4
    response = {
        "thread": thread,
        "user": user
    }
    #cursor.close()
    return make_response(0, response)



@thread.route(BASE_URL + '/unsubscribe/', methods=['POST'])
def unsubscribe():
    try:
        data = request.get_json()
    except ValueError:
        return response_2
    try:
       thread = data['thread']
       user = data['user']
    except (KeyError):
        return response_2
    db = get_db()
    cursor = db.cursor()
    id = Get_subscribe_id(user, thread, cursor)
    if id == -1:
        cursor.close()
        return response_1
    try:
        cursor.execute(get_unsubscribe, [id])
        db.commit()
    except DatabaseError:
        cursor.close()
        return response_4
    response = {
        "thread": thread,
        "user": user
    }
    cursor.close()
    return make_response(0, response)

@thread.route(BASE_URL + '/update/', methods=['POST'])
def update():
    db = get_db()
    cursor = db.cursor()
    try:
        data = request.get_json()
    except ValueError:
        cursor.close()
        return response_2
    try:
       thread = data['thread']
       message  = data['message']
       slug = data['slug']
    except (KeyError):
        cursor.close()
        return response_2
    try:
        cursor.execute(update_thread, [message, slug, thread])
        db.commit()
    except DatabaseError:
        cursor.close()
        return response_4
    response = make_response_for_thread(thread, cursor)
    cursor.close()
    return make_response(0, response)



@thread.route(BASE_URL + '/vote/', methods=['POST'])
def vote():
    db = get_db()
    cursor = db.cursor()
    try:
        data = request.get_json()
    except ValueError:
        cursor.close()
        return response_2
    try:
       thread_id = data['thread']
       vote = data['vote']
    except (KeyError):
        cursor.close()
        return response_2
    if vote == 1:
        query = get_like_for_thread
    elif vote == -1:
        query = get_dislike_for_thread
    else:
        cursor.close()
        return response_2
    try:
        cursor.execute(query, [thread_id])
        db.commit()
    except DatabaseError:
        cursor.close()
        return response_4
    response = make_response_for_thread(thread_id, cursor)
    return make_response(0, response)
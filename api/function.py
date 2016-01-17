__author__ = 'alla'
#import json
from sql import *
import json as ujson
from flask import Response
from thread_queries import data_thread_related_user_forum, data_thread_related_user, data_thread_related_forum, data_thread
from user_queries import get_followeing, get_followers, get_subscriptions
from forum_queries import *


from post_queries import *

def make_response(code, response):
   return jsonify({'code': code, 'response':response})


def jsonify(input_dict):
    return Response(mimetype='application/json', response=ujson.dumps(input_dict))


def make_response_for_user(id, cursor):
    cursor.execute(get_user_by_id, [id])
    data = cursor.fetchall()[0]
    followers = user_followers(data[5], cursor)
    following = user_following(data[5], cursor)
    subscriptions = user_subscriptions(data[5], cursor)
    return {
        "about": data[2],
        "email": data[5],
        "followers": followers,
        "following": following,
        "id": id,
        "isAnonymous": data[3],
        "name": data[0],
        "subscriptions": subscriptions,
        "username": data[1]
    }


def make_response_for_user_by_email(email, cursor):
    cursor.execute(get_user_by_email, [email])
    data = cursor.fetchall()[0]
    followers = user_followers(email, cursor)
    following = user_following(email, cursor)
    subscriptions = user_subscriptions(email, cursor)
    response  = {
        "about": data[2],
        "email": email,
        "followers": followers,
        "following": following,
        "id": data[4],
        "isAnonymous": data[3],
        "name": data[0],
        "subscriptions": subscriptions,
        "username": data[1]
    }
    return response

def make_response_for_post(id, cursor, related):
    cursor.execute(post_data, [id])
    data = cursor.fetchall()[0]
    if 'user' in related:
        user = make_response_for_user_by_email(data[12], cursor)
    else:
        user = data[12]
    if 'forum' in related:
        #forum = make_response_for_forum(data[13], cursor, [])
        forum = make_response_for_forum_by_short_name(data[13], cursor, [])
    else:
        forum = data[13]
    if 'thread' in related:
            thread = make_response_for_thread(data[10], cursor)
    else:
        thread = data[10]
    return {
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


def Get_user_id(email, cursor):
    if(cursor.execute(get_user_id, [email,]) == 0 ):
        return -1
    id = cursor.fetchone()[0]
    return id

def Get_forum_id(short_name, cursor):
    if(cursor.execute(get_forum_id, [short_name]) == 0 ):
        return -1
    id = cursor.fetchone()[0]
    return id

def make_a_response_for_user(data, followers, following, subscriptions):
    return {
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



def make_a_response_for_thread(id, cursor):
    cursor.execute(data_thread, [id])
    data = cursor.fetchall()[0]
    return {
        "date": str(data[3]),
        "dislikes": data[8],
        "forum": data[10],
        "id": data[0],
        "isClosed": data[2],
        "isDeleted": data[6],
        "likes": data[7],
        "message": data[4],
        "points": 0,
        "posts": "",
        "slug": data[5],
        "title": data[1],
        "user": data[9]
    }


def Optional_order(request):
    order = request.args.get('order')
    if order == None or order == 'desc':
        return ' ORDER BY date DESC'
    elif order == 'asc':
        return ' ORDER BY date ASC'
    else:
        return False

def optional_Order(request):
    order = request.args.get('order')
    if order == None or order == 'desc':
        return ' DESC'
    elif order == 'asc':
        return  ' ASC'
    else:
        return ""

def Optional_order_by_id(request):
    order = request.args.get('order')
    if order == None or order == 'desc':
        return ' ORDER BY id DESC'
    elif order == 'asc':
        return  ' ORDER BY id ASC'
    else:
        return ""

def Order_by_user_id(request):
    order = request.args.get('order')
    if order == None or order == 'desc':
        return ' ORDER BY User.id DESC'
    elif order == 'asc':
        return  ' ORDER BY User.id ASC'
    else:
        return ""

def Optional_order_by_mpath(request):
    order = request.args.get('order')
    if order == None or order == 'desc':
        return ' ORDER BY mpath DESC'
    elif order == 'asc':
        return  ' ORDER BY mpath ASC'
    else:
        return ""

def Optional_order_by_name(request):
    order = request.args.get('order')
    if order == None or order == 'desc':
        return ' ORDER BY User.name DESC'
    elif order == 'asc':
        return  ' ORDER BY User.name ASC'
    else:
        return ""


def optional_Limit(request):
    limit = request.args.get('limit')
    if limit != None:
        return ' LIMIT '+limit+";"
    else:
        return ";"


def Optional_sience_date(request):
    since = request.args.get('since')
    if since != None:
        return "AND date >= '%s'" % since
    else:
        return ''




def Optional_sience_id(request):
    since = request.args.get('since')
    if since != None:
        return "AND User_id1 >= %s" % since
    else:
        return ""


def Get_forum_id(short_name, cursor):
    if(cursor.execute(get_forum_id, [short_name]) == 0 ):
        cursor.close()
        return -1
    id = cursor.fetchone()[0]
    return id


def Get_subscribe_id(id1, id2, cursor):
    if(cursor.execute(data_subscribe, [id1,id2]) == 0):
        return -1
    id  = cursor.fetchone()[0]
    return id

def Get_user_follower_followee(id1, id2, cursor):
    if(cursor.execute(get_id_unfollow, [id1,id2]) == 0):
        return -1
    id  = cursor.fetchone()[0]
    return id

def Get_id_follower_followee(email_follower, email_followee, cursor):
    if(cursor.execute(get_id_follower_followee, [email_follower, email_followee]) == 0 ):
        return [-1,-1]
    id = cursor.fetchall()[0]
    return id



def Forum_response(data, user):
    return {
        "id": data[0],
        "name": data[1],
        "short_name": data[2],
        "user": user
        }


def make_response_for_forum_by_short_name(short_name, cursor, related):
    if related == 'user':
        data_forum = cursor.execute(data_forum_by_short_name_related_user, [short_name])
        if(data_forum == 0):
            return None
        data = cursor.fetchall()[0]
        followers = user_followers(data[4], cursor)
        following = user_following(data[4], cursor)
        subscriptions = user_subscriptions(data[4], cursor)
        user = {
        "about": data[7],
        "email": data[4],
        "followers": followers,
        "following": following,
        "id": data[3],
        "isAnonymous": data[8],
        "name": data[5],
        "subscriptions": subscriptions,
        "username": data[6]
        }
    else:
        data_forum = cursor.execute(data_forum_by_short_name, [short_name])
        if(data_forum == 0):
            return None
        data = cursor.fetchall()[0]
        user = data[3]
    return {
        "id": data[0],
        "name": data[1],
        "short_name": data[2],
        "user": user
        }


def Post_reaponse(data, user = "", forum = "", thread = ""):
    if user == "":
        user = data[12]
    if forum == "":
        forum = data[13]
    if thread == "":
        thread = data[10]
    return {
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

def User_reaponse(data, followers, following, subscriptions):
    return {
        "name": data[0],
        "username": data[1],
        "about": data[2],
        "isAnonymous": data[3],
        "id": data[4],
        "email": data[5],
        "followers": followers,
        "following": following,
        "subscriptions": subscriptions
    }

def Thread_reaponse(data, user = "", forum = ""):
    if user == "":
        user = data[10]
    if forum == "":
        forum = data[11]
    return {
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


def user_following(id, cursor):
    cursor.execute(get_followeing,[id])
    result = [i[0] for i in cursor.fetchall()]
    return result

def user_followers(email, cursor):
    cursor.execute(get_followers,[email])
    result = [i[0] for i in cursor.fetchall()]
    return result

def user_subscriptions(id, cursor):
    cursor.execute(get_subscriptions,[id])
    result = [i[0] for i in cursor.fetchall()]
    return result



def make_response_for_thread(id, cursor, related = []):
    if 'user' in related and 'forum' in related:
        query = cursor.execute(data_thread_related_user_forum, [id])
        if(query == 0):
            return None
        data = cursor.fetchall()[0]
        followers = user_followers(data[10], cursor)
        following = user_following(data[10], cursor)
        subscriptions = user_subscriptions(data[10], cursor)
        user =  {
        "about": data[14],
        "email": data[10],
        "followers": followers,
        "following": following,
        "id": data[19],
        "isAnonymous": data[15],
        "name": data[12],
        "subscriptions": subscriptions,
        "username": data[13]
        }
        forum  = {
        "id": data[18],
        "name": data[16],
        "short_name": data[11],
        "user": data[17]
        }
    elif 'user' in related and 'forum' not in related:
        query = cursor.execute(data_thread_related_user, [id])
        if(query == 0):
            return None
        data = cursor.fetchall()[0]
        followers = user_followers(data[10], cursor)
        following = user_following(data[10], cursor)
        subscriptions = user_subscriptions(data[10], cursor)
        user =  {
        "about": data[14],
        "email": data[10],
        "followers": followers,
        "following": following,
        "id": data[16],
        "isAnonymous": data[15],
        "name": data[12],
        "subscriptions": subscriptions,
        "username": data[13]
        }
        forum = data[11]
    elif 'user' not in related and 'forum' in related:
        query = cursor.execute(data_thread_related_forum, [id])
        if(query == 0):
            return None
        data = cursor.fetchall()[0]
        user = data[10]
        forum  = {
        "id": data[12],
        "name": data[13],
        "short_name": data[11],
        "user": data[14]
        }
    else:
        query = cursor.execute(data_thread, [id])
        if(query == 0):
            return None
        data = cursor.fetchall()[0]
        user = data[10]
        forum = data[11]
    return {
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
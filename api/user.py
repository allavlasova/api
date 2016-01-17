__author__ = 'alla'
from flask import Flask, request
from flask import Blueprint
from db import get_db
from function import *
from pymysql import DatabaseError
from user_queries import user_by_email, get_listFollowers, get_listFollowing, get_list_post_by_email, set_follow, set_unfollow, create_user
from response import response_1, response_2, response_4, response_5
user = Blueprint('user', __name__)
BASE_URL = "/user"

@user.route(BASE_URL + '/details/')
def datails():
    cursor = get_db().cursor()
    email = request.args.get('user')
    if(email == None):
        return response_2
    try:
        cursor.execute(user_by_email, [email])
    except DatabaseError:
        cursor.close()
        return response_1
    data = cursor.fetchall()[0]
    followers = user_followers(email, cursor)
    following = user_following(email, cursor)
    subscriptions = user_subscriptions(email, cursor)
    response  = User_reaponse(data, followers, following, subscriptions)
    #cursor.close()
    return make_response(0, response)

@user.route(BASE_URL + '/create/', methods=['POST'])
def create():
    db = get_db()
    cursor = db.cursor()
    try:
        data = request.get_json()
    except ValueError:
        cursor.close()
        return response_2
    try:
        email = data['email']
        username = data['username']
        name = data['name']
        about = data['about']
    except (KeyError):
        cursor.close()
        return response_2
    try:
        isAnonymous = data['isAnonymous']
    except (KeyError):
        isAnonymous = False
    try:
        cursor.execute(create_user,[username, about, name, email, isAnonymous])
        db.commit()
    except (DatabaseError):
        return  response_5
    id = cursor.lastrowid
    responce = {
        "about": about,
        "email": email,
        "id": id,
        "isAnonymous": isAnonymous,
        "name": name,
        "username": username
    }
    #cursor.close()
    return make_response(0, responce)


@user.route(BASE_URL + '/follow/', methods=['GET', 'POST'])
def follow():
    if(request.method == 'GET'):
        return make_response(2, "no valid maethod")
    db = get_db()
    cursor = db.cursor()
    try:
        data = ujson.loads(request.data)
    except ValueError:
        cursor.close()
        return response_2
    try:
        follower = data['follower']
        followee = data['followee']
    except (KeyError):
        cursor.close()
        return response_2
    try:
        cursor.execute(set_follow, [follower, followee])
        db.commit()
    except DatabaseError:
        return response_4
    response = make_response_for_user_by_email(follower, cursor)
    return make_response(0, response)

@user.route(BASE_URL + '/unfollow/', methods=['POST'])
def unfollow():
    db = get_db()
    cursor = db.cursor()
    data = ujson.loads(request.data)
    try:
        follower = data['follower']
        followee = data['followee']
    except (KeyError):
        cursor.close()
        return response_2
    id = Get_user_follower_followee(follower, followee, cursor)
    if id == -1:
        return response_1
    try:
        cursor.execute(set_unfollow,[id, ])
        db.commit()
    except (DatabaseError):
        cursor.close()
        return response_4
    response = make_response_for_user_by_email(follower, cursor)
    #cursor.close()
    return make_response(0, response)

@user.route(BASE_URL + '/listFollowers/')
def listFollowers():
    email = request.args.get('user')
    if(email == None):
        return response_2
    cursor = get_db().cursor()
    since = Optional_sience_id(request)
    add_order = Order_by_user_id(request)
    add_limit = optional_Limit(request)
    if add_order == "":
        cursor.close()
        return response_2
    try:
        cursor.execute(get_listFollowers + add_order + add_limit, [email])
    except (DatabaseError):
        cursor.close()
        return response_4
    list_followers = []
    for data in cursor.fetchall():
        followers = user_followers(data[5], cursor)
        following = user_following(data[5], cursor)
        subscriptions = user_subscriptions(data[5], cursor)
        response  = User_reaponse(data, followers, following, subscriptions)
        list_followers.append(response)
    return make_response(0, list_followers)

@user.route(BASE_URL + '/listFollowing/')
def listFollowing():
    email = request.args.get('user')
    if(email == None):
        return response_2
    cursor = get_db().cursor()
    since = Optional_sience_id(request)
    add_order = Order_by_user_id(request)
    add_limit = optional_Limit(request)
    if add_order == "":
        cursor.close()
        return response_2
    try:
        cursor.execute(get_listFollowing + since + add_order + add_limit,[email])
    except (DatabaseError):
        cursor.close()
        return response_4
    list_following = []
    for data in cursor.fetchall():
        followers = user_followers(data[5], cursor)
        following = user_following(data[5], cursor)
        subscriptions = user_subscriptions(data[5], cursor)
        response  = User_reaponse(data, followers, following, subscriptions)
        list_following.append(response)
    return make_response(0, list_following)



@user.route(BASE_URL + '/listPosts/')
def listPosts():
    email = request.args.get('user')
    if(email == None):
        return response_2
    cursor = get_db().cursor()
    add_order = Optional_order(request)
    if add_order == False:
        cursor.close()
        return response_2
    since = Optional_sience_date(request)
    add_limit = optional_Limit(request)
    try:
        cursor.execute(get_list_post_by_email + since + add_order + add_limit,[email])
    except DatabaseError:
        cursor.close()
        return response_4
    list_posts = []
    for data in cursor.fetchall():
        post = Post_reaponse(data)
        list_posts.append(post)
    return make_response(0, list_posts)


@user.route(BASE_URL + '/updateProfile/', methods=['POST'])
def updateProfile():
    db = get_db()
    cursor = db.cursor()
    data = ujson.loads(request.data)
    try:
        email = data['user']
        name = data['name']
        about = data['about']
    except (KeyError):
        cursor.close()
        return response_2
    id = Get_user_id(email, cursor)
    if id == -1:
        cursor.close()
        return response_1
    try:
        cursor.execute(update_profule, [about, name, id])
        db.commit()
    except (DatabaseError):
        return  response_4
    response = make_response_for_user(id, cursor)
    cursor.close()
    return make_response(0, response)




__author__ = 'alla'

create_user = "INSERT INTO User (username, about, name, email, isAnonymous) VALUES (%s, %s, %s, %s, %s);"


user_by_email = "SELECT name, username, about, isAnonymous, id, email FROM User WHERE email = %s;"

get_followers = "SELECT follower FROM followers WHERE followee = %s;"

get_followeing = "SELECT followee FROM followers WHERE follower = %s;"

get_subscriptions = '''SELECT Thread_id FROM subscriptions  WHERE user = %s'''

get_listFollowers = '''SELECT  name, username, about, isAnonymous, User.id, email FROM User
                JOIN
                followers
                ON User.email = followers.follower  WHERE followee =%s '''

get_listFollowing = '''SELECT  name, username, about, isAnonymous, User.id, email FROM User
                JOIN
                followers
                ON User.email = followers.followee  WHERE follower =%s '''

get_list_post_by_email = '''SELECT Post.id, date, message, isApporved, isDeleted, isEdited, isHighlighted, isSpam,
dislikes, likes, Post.Thread_id, parent, Post.user, Post.forum FROM Post WHERE Post.user = %s '''


set_follow = "INSERT LOW_PRIORITY  INTO followers (follower, followee) VALUES (%s, %s)"

set_unfollow = "DELETE LOW_PRIORITY  FROM followers WHERE id= %s;"

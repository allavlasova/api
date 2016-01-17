__author__ = 'alla'

user_by_id =  "SELECT email FROM User WHERE id = %s;"

forum_by_id =  "SELECT Forum.short_name FROM Forum WHERE id = %s;"

get_user_by_email = "SELECT name, username, about, isAnonymous, id FROM User WHERE email = %s;"

get_user_id = "SELECT id FROM User WHERE email = %s;"

get_user_by_id = "SELECT name, username, about, isAnonymous, id, email FROM User WHERE id = %s;"



set_unfollow = "DELETE FROM followers WHERE `id`= %s;"


update_profule = "UPDATE User SET about=%s, `name`=%s WHERE `id`=%s;"

get_forum_id = "SELECT id FROM Forum WHERE short_name = %s;"



get_thread_id = "SELECT id FROM Thread WHERE id = %s;"

get_last = "SELECT MAX(id) FROM Post"

get_last_id_for_thread = "SELECT MAX(id) FROM Thread"

get_forum = "SELECT short_name FROM Forum WHERE id = %s"



list_post_id = "SELECT Post.id FROM Forum INNER JOIN Post ON Post.Forum_id = Forum.id WHERE Forum.id = %s;"

list_id_post = "SELECT Post.id FROM Forum INNER JOIN Post ON Post.Forum_id = Forum.id WHERE Forum.short_name = %s"

list_id_post1 = "SELECT Post.id FROM Forum INNER JOIN Post ON Post.Forum_id = Forum.id WHERE Forum.id = %s ORDER BY date"

list_id_post_by_thread_id = "SELECT Post.id FROM Post WHERE Thread_id = %s "




list_id_post_by_thread_id1 = "SELECT Post.id FROM Post WHERE Thread_id = %s"


get_list_post_id_by_forum_short_name = 'SELECT Post.id FROM Forum INNER JOIN Post ON Post.Forum_id = Forum.id WHERE Forum.short_name = %s;'

get_list_post_id_by_thread = "SELECT Post.id FROM Post WHERE Post.Thread_id = %s  AND date >= %s "

get_list_post_id_by_thread1 = "SELECT Post.id FROM Post WHERE Post.Thread_id = %s "


get_list_post_by_forum_id = "SELECT Post.id FROM Post WHERE Post.Forum_id = %s  AND date >= %s"

get_list_post_by_forum_short_name = "SELECT Post.id FROM Post JOIN Forum ON Post.Forum_id = Forum.id WHERE Forum.short_name = %s "

get_list_post_by_forum_id = "SELECT Post.id FROM Post WHERE Forum_id = %s "



get_list_post_by_forum_id1 = "SELECT Post.id FROM Post WHERE Post.Forum_id = %s"

get_list_thread_by_forum_id = "SELECT Thread.id FROM Thread WHERE Thread.Forum_id = %s  AND date >= %s"

get_list_thread_by_forum_short_name = '''SELECT Thread.id FROM Thread JOIN Forum ON Forum.id = Thread.Forum_id
WHERE Forum.short_name = %s'''


get_list_thread_by_forum_id1 = "SELECT Thread.id FROM Thread WHERE Thread.Forum_id = %s"



data_subscribe = "SELECT subscriptions.id FROM subscriptions WHERE user = %s AND Thread_id = %s;"



get_id_unfollow = "SELECT id FROM followers WHERE follower = %s AND followee = %s;"



get_isDelete = "SELECT isDeleted FROM Post WHERE id = %s"


get_id_follower_followee = '''SELECT u1.id, u2.id FROM User AS u1
JOIN
User AS u2 WHERE u1.email = %s AND u2.email=%s;'''





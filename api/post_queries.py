__author__ = 'alla'

get_post_id = "SELECT id FROM Post WHERE id = %s;"


create_post = '''INSERT INTO Post (date, Thread_id, message, user, forum, parent, isApporved, isHighlighted, isEdited, isSpam, isDeleted)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''


post_data = '''SELECT Post.id, date, message, isApporved, isDeleted,
                        isEdited, isHighlighted, isSpam, dislikes, likes,
                        Post.Thread_id, parent,
                        Post.user, Post.forum FROM Post
                        WHERE Post.id = %s;'''


get_list_post_data_by_forum = '''SELECT  Post.id, date, message, isApporved, isDeleted,
                        isEdited, isHighlighted, isSpam, dislikes, likes,
                        Post.Thread_id, parent, Post.user,
                        Post.forum FROM Post WHERE Post.forum = %s '''

get_list_post_data_by_thread = '''SELECT  Post.id, date, message, isApporved, isDeleted,
                        isEdited, isHighlighted, isSpam, dislikes, likes,
                        Post.Thread_id, parent, Post.user,
                        Post.forum FROM Post WHERE Post.Thread_id = %s '''


remove_post = "UPDATE Post SET isDeleted = 1 WHERE id = %s;"

restore_post = "UPDATE Post SET isDeleted = 0 WHERE id = %s;"

update_post = "UPDATE Post SET message = %s WHERE id =  %s;"


get_like = "UPDATE Post SET likes=likes+1 WHERE id=%s;"

get_dislike = "UPDATE Post SET dislikes = dislikes + 1 WHERE id=%s;"
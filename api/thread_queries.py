
data_thread_related_user_forum = '''SELECT Thread.id, Thread.title, Thread.isClosed, Thread.date,
                        Thread.message, Thread.slug, Thread.isDeleted, Thread.likes,
                        Thread.dislikes,Thread.posts, Thread.user, Thread.forum,
                        U1.name, U1.username, U1.about, U1.isAnonymous,
                        Forum.name, Forum.user, Forum.id, U1.id
                        FROM Thread
                        INNER JOIN Forum ON Forum.short_name = Thread.forum
                        INNER JOIN User AS U1 ON Thread.user = U1.email
                        WHERE Thread.id = %s ; '''

data_thread_related_user = '''SELECT Thread.id, Thread.title, Thread.isClosed, Thread.date,
                        Thread.message, Thread.slug, Thread.isDeleted, Thread.likes,
                        Thread.dislikes,Thread.posts, Thread.user, Thread.Forum,
                        User.name, User.username, User.about, User.isAnonymous, User.id FROM Thread
                        INNER JOIN User ON Thread.user = User.email
                        WHERE Thread.id = %s ; '''

data_thread_related_forum = '''SELECT Thread.id, Thread.title, Thread.isClosed, Thread.date,
                        Thread.message, Thread.slug, Thread.isDeleted, Thread.likes,
                        Thread.dislikes, Thread.posts, Thread.user, Thread.forum, Forum.id, Forum.name, Forum.user
                        FROM Thread
                        INNER JOIN
                        Forum ON Forum.short_name = Thread.forum
                        WHERE Thread.id = %s;'''

data_thread = '''SELECT Thread.id, Thread.title, Thread.isClosed, Thread.date,
                        Thread.message, Thread.slug, Thread.isDeleted, Thread.likes,
                        Thread.dislikes, Thread.posts,
                        Thread.user, Thread.forum
                        FROM Thread
                        WHERE Thread.id = %s;'''

close_thread = "UPDATE LOW_PRIORITY  Thread  SET  isClosed ='1' WHERE id= %s;"


get_like_for_thread = "UPDATE Thread SET likes=likes+1 WHERE id=%s;"

get_dislike_for_thread = "UPDATE Thread SET dislikes = dislikes + 1 WHERE id=%s;"

update_thread = "UPDATE Thread SET message= %s, slug = %s WHERE id = %s;"


get_unsubscribe = "DELETE FROM subscriptions WHERE id = %s ;"

get_subscribe = "INSERT INTO subscriptions (user, Thread_id) VALUES (%s, %s);"


restore_thread = "UPDATE Thread  SET  isDeleted = False WHERE `id`= %s;"

restore_the_posts_in_the_thread = "UPDATE Post SET `isDeleted`='0' WHERE Thread_id= %s;"

remove_thread = "UPDATE Thread  SET  isDeleted = True WHERE `id`= %s;"

remove_the_posts_in_the_thread = "UPDATE Post SET `isDeleted`='1' WHERE Thread_id= %s;"


get_list_thread_data_by_user_email = '''SELECT Thread.id, Thread.title, Thread.isClosed, Thread.date,
                        Thread.message, Thread.slug, Thread.isDeleted, Thread.likes,
                        Thread.dislikes, Thread.posts,
                        Thread.user, Thread.forum
                        FROM Thread
                        WHERE Thread.user = %s '''


list_data_post_by_thread_id = '''SELECT Post.id, Post.date, Post.message, Post.isApporved, Post.isDeleted,
                        Post.isEdited, Post.isHighlighted, Post.isSpam, Post.dislikes, Post.likes,
                        Post.Thread_id, parent, Post.user, Post.forum
                        FROM Post WHERE Post.Thread_id = %s '''


get_list_thread_data_by_forum_short_name = '''SELECT Thread.id, Thread.title, Thread.isClosed, Thread.date,
                        Thread.message, Thread.slug, Thread.isDeleted, Thread.likes,
                        Thread.dislikes, Thread.posts,
                        Thread.user, Thread.forum
                        FROM Thread
                        WHERE Thread.forum = %s '''



posts_by_thread_id_related_user_forum = '''SELECT Post.id, Post.date, Post.message, Post.isApporved, Post.isDeleted,
                        Post.isEdited, Post.isHighlighted, Post.isSpam, Post.dislikes, Post.likes,
                        Post.Thread_id, parent, Post.user, Post.forum,
                        User.name, User.username, User.about, User.isAnonymous, User.id ,  Forum.name, Forum.user, Forum.id
                        FROM Post
                        LEFT JOIN User ON Post.user = User.email
                        JOIN Forum
                        ON Post.forum = Forum.short_name
                        WHERE Post.Thread_id = %s '''

posts_by_thread_id_related_forum = '''SELECT Post.id, Post.date, Post.message, Post.isApporved, Post.isDeleted,
                        Post.isEdited, Post.isHighlighted, Post.isSpam, Post.dislikes, Post.likes,
                        Post.Thread_id, parent, Post.user, Post.forum,
                        Forum.name, Forum.user, Forum.id
                        JOIN Forum
                        ON Post.forum = Forum.short_name
                        WHERE Post.Thread_id = %s '''

posts_by_thread_id_related_user = '''SELECT Post.id, Post.date, Post.message, Post.isApporved, Post.isDeleted,
                        Post.isEdited, Post.isHighlighted, Post.isSpam, Post.dislikes, Post.likes,
                        Post.Thread_id, parent, Post.user, Post.forum,
                        User.name, User.username, User.about, User.isAnonymous, User.id
                        FROM Post
                        LEFT JOIN User ON Post.user = User.email
                        WHERE Post.Thread_id = %s '''

open_thread = "UPDATE Thread  SET  isClosed ='0' WHERE `id`= %s;"

create_thread = "INSERT LOW_PRIORITY  INTO Thread (title, date, message, slug, user, forum, isClosed, isDeleted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
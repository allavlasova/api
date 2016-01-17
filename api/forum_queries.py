__author__ = 'alla'


create_forum = '''INSERT INTO Forum (name, short_name, user) VALUES (%s, %s, %s);'''


list_data_post_related_user_thread = '''SELECT sql_cache Post.id, Post.date, Post.message, Post.isApporved,
Post.isDeleted, Post.isEdited, Post.isHighlighted, Post.isSpam,
Post.dislikes, Post.likes, Post.Thread_id, Post.parent, Post.user, Post.forum,
Thread.id, Thread.title, Thread.isClosed, Thread.date,
Thread.message, Thread.slug, Thread.isDeleted, Thread.likes, Thread.dislikes, Thread.posts,
Thread.user, Thread.forum,
User.name, User.username, User.about, User.isAnonymous, User.id
FROM Post
LEFT JOIN
User ON User.email = Post.User
JOIN
Thread ON Thread.id = Post.Thread_id
WHERE Post.forum = %s '''


list_data_post = '''SELECT sql_cache Post.id, date, message, isApporved, isDeleted, isEdited, isHighlighted, isSpam,
dislikes, likes, Post.Thread_id, parent, Post.user, Post.forum FROM Post WHERE Post.forum = %s '''



data_thread_by_forum_short_name = '''SELECT Thread.id, Thread.title, Thread.isClosed, Thread.date,
                        Thread.message, Thread.slug, Thread.isDeleted, Thread.likes,
                        Thread.dislikes, Thread.posts,
                        Thread.user, Thread.forum
                        FROM Thread
                        WHERE Thread.forum = %s '''


data_forum_by_short_name = '''SELECT Forum.id, Forum.name, Forum.short_name, Forum.user
                FROM Forum  WHERE Forum.short_name = %s;'''



data_forum_by_short_name_related_user = '''SELECT Forum.id, Forum.name, Forum.short_name, User.id, Forum.user,
                                    User.name, User.username, User.about, User.isAnonymous FROM Forum
                                    INNER JOIN User ON Forum.user = User.email WHERE Forum.short_name = %s;'''


user_list = "SELECT User.name, username, about, isAnonymous, id, email FROM User JOIN user_forum ON User.id = user_forum.user_id WHERE user_forum.forum = %s "
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    post = 'P'
    news = 'N'

    POSITIONS = [
        (post, 'Статья'),
        (news, 'Новость')
    ]
    # связь «один ко многим» с моделью Author;
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    # поле с выбором статья или новость
    position = models.CharField(max_length=1, choices=POSITIONS, default=news)
    # автоматически добавляемая дата и время создания;
    time_create = models.DateTimeField(auto_now_add=True)
    # заголовок статьи;
    post_headline = models.CharField(max_length=255, default="Заголовок не указан")
    # заголовок новости;
    news_headline = models.CharField(max_length=255, default="Заголовок не указан")
    # текст статьи;
    post_text = models.TextField(default="Текст статьи временно недоступен")
    # текст новости;
    news_text = models.TextField(default="Текст статьи временно недоступен")
    # рейтинг статьи.
    posts_rating = models.IntegerField(default=0.0)
    # рейтинг новости.
    news_rating = models.IntegerField(default=0.0)
    # связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
    categorys = models.ManyToManyField("Category", through='PostCategory')
    # поле с выбором — «статья» или «новость»;

    def like(self):
        self.posts_rating += 1
        self.news_rating += 1
        self.save()

    def dislike(self):
        self.posts_rating -= 1
        self.news_rating -= 1
        self.save()

    def preview(self):
        return self.post_text[:123]


class PostCategory(models.Model):
    # связь «один ко многим» с моделью Post;
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # связь «один ко многим» с моделью Category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comments_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commenst_user = models.ForeignKey(User, on_delete=models.CASCADE)
    commenst = models.TextField()
    com_time_create = models.DateTimeField(auto_now_add=True)
    comments_rating = models.IntegerField(default=0.0)

    def like(self):
        self.comments_rating += 1
        self.save()

    def dislike(self):
        self.comments_rating -= 1
        self.save()


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.FloatField(default=0.0)
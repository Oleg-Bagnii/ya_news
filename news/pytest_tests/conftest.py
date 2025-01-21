import pytest

# Импортируем класс клиента.
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from datetime import datetime, timedelta
from news.models import News, Comment
from news.forms import BAD_WORDS, WARNING


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):  # Вызываем фикстуру автора.
    client = Client()
    client.force_login(author)  # Логиним автора в клиенте.
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)  # Логиним обычного пользователя в клиенте.
    return client


@pytest.fixture
def news():
    news = News.objects.create(  # Создаём объект заметки.
        title='Заголовок',
        text='Текст заметки'
    )
    return news


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(news=news, author=author,
                                     text='Текст комментария')
    return comment


@pytest.fixture
def url_delete(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def url_edit(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def url_detail(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def eleven_news(news):
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    return News.objects.bulk_create(all_news)


@pytest.fixture
def comment_text():
    return 'Текст комментария'


@pytest.fixture
def new_comment_text():
    return 'Обновлённый комментарий'

@pytest.fixture
def form_data(comment_text):
    return {'text': comment_text}


@pytest.fixture
def bad_worlds():
    return BAD_WORDS


@pytest.fixture
def warning():
    return WARNING

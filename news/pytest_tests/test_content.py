import pytest

from pytest_django.asserts import assertRedirects

from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm


@pytest.mark.django_db
def test_news_count(eleven_news, client):
    response = client.get(reverse('news:home'))
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(eleven_news, client):
    response = client.get(reverse('news:home'))
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, url_detail):
    response = client.get(url_detail)
    print(response.context)
    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_client_has_form(author_client, url_detail):
    response = author_client.get(url_detail)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


@pytest.mark.django_db
def test_comments_order(client, url_detail):
    response = client.get(url_detail)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps

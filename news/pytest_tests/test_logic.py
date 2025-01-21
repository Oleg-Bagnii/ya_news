import pytest

from http import HTTPStatus

from pytest_django.asserts import assertRedirects, assertFormError

from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(form_data, url_detail, client):
    client.post(url_detail, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_can_create_comment(form_data, author_client, url_detail, author,
                                 news, comment_text):
    response = author_client.post(url_detail, data=form_data)
    assertRedirects(response, f'{url_detail}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == comment_text
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(bad_worlds, author_client, url_detail,
                                 warning):
    bad_words_data = {'text': f'Какой-то текст, {bad_worlds[0]}, еще текст'}
    response = author_client.post(url_detail, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=warning
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(author_client, url_detail, url_delete):
    response = author_client.delete(url_delete)
    assertRedirects(response, url_detail + '#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_delete_comment_of_another_user(not_author_client,
                                                  url_delete):
    response = not_author_client.delete(url_delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_author_can_edit_comment(form_data, url_edit, author_client, comment,
                                 url_detail, comment_text):
    response = author_client.post(url_edit, data=form_data)
    assertRedirects(response, url_detail + '#comments')
    comment.refresh_from_db()
    assert comment.text == comment_text


def test_user_cant_edit_comment_of_another_user(not_author_client, url_edit,
                                                form_data, comment,
                                                comment_text):
    response = not_author_client.post(url_edit, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == comment_text

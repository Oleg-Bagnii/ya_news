import pytest

from pytest_django.asserts import assertRedirects

from http import HTTPStatus

from django.urls import reverse


# Указываем в фикстурах встроенный клиент.
@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',  # Имя параметра функции.
    # Значения, которые будут передаваться в name.
    ('news:home', 'users:login', 'users:logout', 'users:signup')
)
def test_home_availability_for_anonymous_user(client, name):
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_detail_page_for_anonymous_user(client, url_detail):
    response = client.get(url_detail)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    ((pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND), (pytest.lazy_fixture('author_client'), HTTPStatus.OK)),
    )
@pytest.mark.parametrize('name', ('news:edit', 'news:delete'))
def test_availability_for_comment_edit_and_delete(author_client,
                                                  not_author_client,
                                                  comment, name, parametrized_client, expected_status):
    url = reverse(name, args=(comment.id,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize('name', ('news:edit', 'news:delete'))
def test_redirect_for_anonymous_client(name, comment, client):
    login_url = reverse('users:login')
    url = reverse(name, args=(comment.id,))
    redirect_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, redirect_url)

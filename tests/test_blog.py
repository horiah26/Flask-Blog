"""Post tests"""
from werkzeug.datastructures import FileStorage
from conftest import login, logout


def test_homepage_works(client):
    """Tests if homepage works"""
    rv = client.get('/')
    assert b'blog-description' in rv.data
    assert b'wrapper' in rv.data
    assert b'welcome' in rv.data
    assert b'category-tag popular' in rv.data
    assert b'profile-img' in rv.data


def test_statistics_page_works(client):
    """Tests that statistics are shown correctly"""
    login(client, 'admin', 'admin')

    rv = client.get('/statistics')
    print(rv.data)
    assert b"""<td class="month">2021-6</td>\n        <td class="posts">5</td>\n    </tr>\n    \n    <tr>\n        <td class="month">2021-1</td>\n        <td class="posts">5</td>\n    </tr>\n    \n    <tr>\n        <td class="month">2020-5</td>\n        <td class="posts">4</td>\n""" in rv.data


def test_cannot_access_statistics_if_not_logged_in(client):
    """Tests cannot access statistics if not logged in"""
    logout(client)
    rv = client.get('/statistics', follow_redirects=True)
    assert b'You must be logged in to do this' in rv.data


def test_shows_message_on_statistics_page_if_user_has_no_posts(client):
    """Shows message if you have no posts yet on statistics page"""
    login(client, 'username4', 'password4')
    rv = client.get('/statistics', follow_redirects=True)
    assert b'You have no posts yet' in rv.data


def test_post_default_image_shown(client):
    """Tests if posts show default image 0.png"""
    rv = client.get('/')
    assert b'src="static/uploads/0.png"' in rv.data


def test_can_change_post_image(client):
    """Tests can change post image"""

    login(client, 'username2', 'password2')
    rv = client.get('/')
    assert b'src="static/uploads/1.png"' not in rv.data

    with open('static/test_pic/test.png', 'rb') as fp:
        image = FileStorage(fp)

        response = client.post('/10/update',
                               follow_redirects=True,
                               content_type='multipart/form-data',
                               data=dict(text='text',
                                         title='title',
                                         img=image))
        print(response.data)
        assert b'src="static/uploads/1.png"' in response.data


def test_can_add_post_with_image(client):
    """Can add a new post with image"""

    login(client, 'username2', 'password2')
    rv = client.get('/')
    assert b'src="static/uploads/1.png"' not in rv.data

    with open('static/test_pic/test.png', 'rb') as fp:
        image = FileStorage(fp)

        response = client.post('/create',
                               follow_redirects=True,
                               content_type='multipart/form-data',
                               data=dict(text='text',
                                         title='title',
                                         img=image))
        print(response.data)
        assert b'src="static/uploads/1.png"' in response.data


def test_cannot_change_post_image_if_txt_extension(client):
    """Tests post doesn't work if extension not in allowed extensions list"""

    login(client, 'username2', 'password2')
    rv = client.get('/')
    assert b'src="static/uploads/1.png"' not in rv.data

    with open('static/test_pic/test.txt', 'rb') as fp:
        image = FileStorage(fp)

        response = client.post('/11/update',
                               follow_redirects=True,
                               content_type='multipart/form-data',
                               data=dict(text='text',
                                         title='title',
                                         img=image))
        print(response.data)
        assert b'src="static/uploads/1.png"' not in rv.data
        assert b'File format not supported. Format must be one of the following: png, jpg, jpeg, gif, bmp' in response.data


def test_display_name_not_username_shown_in_cards(client):
    """Display name is shown in cards"""
    rv = client.get('/')
    assert b' <h6 class="owner">\n                            Name 2\n                        </h6>' in rv.data


def test_opens_first_post_from_seed(client):
    """Can open the first post from seed"""
    assert client.get('/1/').status_code == 200


def test_opens_last_post_from_seed(client):
    """Can open the last post from seed"""
    assert client.get('/14/').status_code == 200


def test_write_article(client):
    """Writes a new article"""
    login(client, 'username1', 'password1')

    client.post('/create',
                data=dict(title='any title',
                          text='any text'))

    assert client.get('/15/', follow_redirects=True).status_code == 200

    logout(client)


def test_does_not_write_article_with_empty_title(client):
    """Does not write article with empty title"""
    login(client, 'username1', 'password1')

    assert client.get('/14/').status_code == 200

    assert b'Title is required' in client.post('/create',
                                               data=dict(title=' ',
                                                         text='Ugly text for test asfjkoas.fnklwpgow[gp[g;pq'),
                                               follow_redirects=True).data


def test_does_not_write_article_if_not_logged_in(client):
    """Cannot write article if not logged_in"""
    redirect = client.post('/create',
                           data=dict(title='Ugly title for test lsdkhnsdpbjeri',
                                     text='Ugly text for test asfjkoas.fnklwpgow[gp[g;pq'), follow_redirects=True)

    assert b'You must be logged in to do this' in redirect.data


def test_cannot_delete_post_if_not_logged_in(client):
    """Cannot delete post if not logged in"""
    logout(client)
    assert client.get('/3/').status_code == 200

    rv = client.get('/3/delete', follow_redirects=True)
    assert b'You don&#39;t have permission to modify this post' in rv.data


def test_cannot_delete_post_if_logged_in_as_another_user(client):
    """Cannot delete post if logged in as another user"""
    rv = login(client, 'username2', 'password2')
    assert client.get('/3/').status_code == 200

    rv = client.get('/3/delete', follow_redirects=True)
    assert b'You don&#39;t have permission to modify this post' in rv.data

    logout(client)


def test_can_delete_own_post_if_logged_in(client):
    """Can delete own post if logged in"""
    login(client, 'username1', 'password1')
    assert client.get('/3/').status_code == 200

    assert b'Post has been deleted' in client.get('/3/delete', follow_redirects=True).data


def test_paging_works(client):
    """Paging works"""
    rv = client.get('/?page=1')
    assert b'id="active-page">1</a>' in rv.data
    assert b'id="inactive-page">2</a>' in rv.data
    assert b'id="inactive-page">3</a>' in rv.data

    assert b'Vivamus pretium dui' in rv.data
    assert b'Nullam quis quam convallis' not in rv.data
    assert b'Lorem ipsum dolor sit amet, consectetur adipiscing elit' not in rv.data

    rv = client.get('/?page=2')
    assert b'id="inactive-page">1</a>' in rv.data
    assert b'id="active-page">2</a>' in rv.data
    assert b'id="inactive-page">3</a>' in rv.data

    assert b'Vivamus pretium dui' not in rv.data
    assert b'Nullam quis quam convallis' in rv.data
    assert b'Lorem ipsum dolor sit amet, consectetur adipiscing elit' not in rv.data

    rv = client.get('/?page=3')
    assert b'id="inactive-page">1</a>' in rv.data
    assert b'id="inactive-page">2</a>' in rv.data
    assert b'id="active-page">3</a>' in rv.data

    assert b'Vivamus pretium dui' not in rv.data
    assert b'Nullam quis quam convallis' not in rv.data
    assert b'Lorem ipsum dolor sit amet, consectetur adipiscing elit' in rv.data


def test_shows_both_arrows_if_not_first_or_last_page(client):
    """Shows both arrows if not first or last page"""
    rv = client.get('/?page=2')
    assert b'&laquo' in rv.data
    assert b'&raquo' in rv.data


def test_shows_only_right_arrow_if_first_page(client):
    """Shows only right arrow if first page"""
    rv = client.get('/?page=1')
    assert b'&laquo' not in rv.data
    assert b'&raquo' in rv.data


def test_shows_only_left_arrow_if_last_page(client):
    """Shows only left arrow if last page"""
    rv = client.get('/?page=3')
    assert b'&laquo' in rv.data
    assert b'&raquo' not in rv.data


def test_filter_works(client):
    """Filter posts by user works"""
    with client.session_transaction() as session:
        session['filter_user'] = 'username1'
    rv = client.get('/')

    assert b'Name 1\'s posts' in rv.data

    assert b'Duis a lectus' in rv.data
    assert b'Aliquam at leo' in rv.data
    assert b'Pellentesque tincidunt' in rv.data
    assert b'Lorem Ipsum' in rv.data

    assert b'In et leo ac erat' not in rv.data
    assert b'Sed quis tellus luctus' not in rv.data
    assert b'Vivamus pretium dui' not in rv.data
    assert b'In et leo ac erat' not in rv.data


def test_doesnt_show_pagination_section_if_only_one_page(client):
    """Doesn't show pagination section if single page"""
    with client.session_transaction() as session:
        session['filter_user'] = 'username1'
    rv = client.get('/')
    print(rv.data)
    assert b'&laquo' not in rv.data
    assert b'&raquo' not in rv.data

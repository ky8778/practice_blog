from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post, Category, Tag, Comment

# Create your tests here.

class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_trump = User.objects.create_user(username='trump', password='somepassword')
        self.user_obama = User.objects.create_user(username='obama', password='somepassword')
        self.user_obama.is_staff = True
        self.user_obama.save()

        self.category_programming = Category.objects.create(name='programming', slug='programming')
        self.category_music = Category.objects.create(name='music', slug='music')

        self.tag_python_kor = Tag.objects.create(name='python_kor', slug='python_kor')
        self.tag_python = Tag.objects.create(name='Python', slug='python')
        self.tag_hello = Tag.objects.create(name='hello', slug='hello')

        self.post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World. We are the world.',
            category=self.category_programming,
            author=self.user_trump,
        )
        self.post_001.tags.add(self.tag_hello)

        self.post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content='2등도 있어요',
            category=self.category_music,
            author=self.user_obama,
        )

        self.post_003 = Post.objects.create(
            title='세 번째 포스트입니다.',
            content='category도 있어요',
            author=self.user_obama,
        )
        self.post_003.tags.add(self.tag_python_kor)
        self.post_003.tags.add(self.tag_python)

        self.comment_001 = Comment.objects.create(
            post=self.post_001,
            author=self.user_obama,
            content='This is first comment'
        )

    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        logo_btn = navbar.find('a', text='KY')
        self.assertEqual(logo_btn.attrs['href'], '/')

        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')

        home_btn = navbar.find('a', text='Blog')
        self.assertEqual(home_btn.attrs['href'], '/blog/')

        home_btn = navbar.find('a', text='About Me')
        self.assertEqual(home_btn.attrs['href'], '/about_me/')

    def category_card_test(self, soup):
        categories_card = soup.find('div', id='categories-card')
        self.assertIn('Categories', categories_card.text)
        self.assertIn(f'{self.category_programming.name} ({self.category_programming.post_set.count()})', categories_card.text)
        self.assertIn(f'{self.category_music.name} ({self.category_music.post_set.count()})', categories_card.text)
        self.assertIn(f'미분류 (1)', categories_card.text)

    def test_post_list(self):
        # 포스트가 있는 경우
        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)

        post_001_card = main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)
        self.assertIn(self.tag_hello.name, post_001_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_001_card.text)
        self.assertNotIn(self.tag_python.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        self.assertNotIn(self.tag_hello.name, post_002_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_002_card.text)
        self.assertNotIn(self.tag_python.name, post_001_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn('미분류', post_003_card.text)
        self.assertNotIn(self.tag_hello.name, post_003_card.text)
        self.assertIn(self.tag_python_kor.name, post_003_card.text)
        self.assertIn(self.tag_python.name, post_003_card.text)

        self.assertIn(self.user_trump.username.upper(), main_area.text)
        self.assertIn(self.user_obama.username.upper(), main_area.text)

        # 포스트가 없는 경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)

        ''' 이전버전
        # 1.1 포스트 목록 페이지를 가져온다.
        response = self.client.get('/blog/')
        # 1.2 정상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code, 200)
        # 1.3 페이지 타이틀은 'Blog'이다.
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')

        # 1.4 내비게이션 바가 있다.
        # navbar = soup.nav
        # 1.5 Blog, About Me라는 문구가 내비게이션 바에 있다.
        # self.assertIn('Blog', navbar.text)
        # self.assertIn('About Me', navbar.text)
        self.navbar_test(soup)

        # 2.1 포스트(게시물)가 하나도 없다면
        self.assertEqual(Post.objects.count(), 0)
        # 2.2 main area에 '아직 게시물이 없습니다'라는 문구가 나타난다.
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)

        # 3.1 포스트가 2개 있다면
        post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World. We are the world.',
            author=self.user_trump,
        )
        post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content='1등이 전부는 아니잖아요?',
            author=self.user_obama
        )
        self.assertEqual(Post.objects.count(), 2)

        # 3.2 포스트 목록 페이지를 새로고침했을 때
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)
        # 3.3 main area에 포스트 2개의 재목이 존재한다.
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        # 3.4 '아직 게시물이 없습니다'라는 문구는 더 이상 나타나지 않는다.
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)

        self.assertIn(self.user_trump.username.upper(), main_area.text)
        self.assertIn(self.user_obama.username.upper(), main_area.text)
        '''

    def test_post_detail(self):
        # 1.1 Post가 하나 있다.
        # post_000 = Post.objects.create(
        #     title='첫 번째 포스트입니다.',
        #     content='Hello World. We are the world.',
        #     author=self.user_trump,
        # )
        # 1.2 그 포스트의 url은 'blog/1/'이다.
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        # 2. 첫 번째 포스트의 상세 페이지 테스트
        # 2.1 첫 번째 post url로 접근하면 정상적으로 작동한다.(status code:200).
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 2.2 포스트 목록 페이지와 똑같은 내비게이션 바가 있다.
        # navbar = soup.nav
        # self.assertIn('Blog', navbar.text)
        # self.assertIn('About Me', navbar.text)
        self.navbar_test(soup)

        # category list test
        self.category_card_test(soup)

        # 2.3 첫 번째 포스트의 제목(title)이 웹 브라우저 탭 타이틀에 들어 있다.
        self.assertIn(self.post_001.title, soup.title.text)

        # 2.4 첫 번째 포스트의 제목이 포스트 영역(post_area)에 있다.
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.category_programming.name, post_area.text)
        self.assertIn(self.tag_hello.name, post_area.text)
        self.assertNotIn(self.tag_python_kor.name, post_area.text)
        self.assertNotIn(self.tag_python.name, post_area.text)

        # 2.5 첫 번째 포스트의 작성자(author)가 포스트 영역에 있다.
        # 아직 작성 불가.

        # 2.6 첫 번째 포스트의 내용(content)이 포스트 영역에 있다.
        self.assertIn(self.post_001.content, post_area.text)
        self.assertIn(self.user_trump.username.upper(), post_area.text)

        # comment area
        comments_area = soup.find('div', id='comment-area')
        comment_001_area = comments_area.find('div', id='comment-1')
        self.assertIn(self.comment_001.author.username, comment_001_area.text)
        self.assertIn(self.comment_001.content, comment_001_area.text)

    def test_category_page(self):
        response = self.client.get(self.category_programming.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.category_programming.name, soup.h3.text)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.category_programming.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    def test_tag_page(self):
        response = self.client.get(self.tag_hello.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.tag_hello.name, soup.h3.text)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.tag_hello.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    def test_create_post(self):
        # 로그인 전 status code가 200이면 안됨.
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

        # staff가 아닌 turmp 로그인을 한다.
        self.client.login(username='trump', password='somepassword')
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

        # staff인 obama 로그인.
        self.client.login(username='obama', password='somepassword')
        response = self.client.get('/blog/create_post/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Create Post - Blog', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Create New Post', main_area.text)

        tag_str_input = main_area.find('input', id='id_tags_str')
        self.assertTrue(tag_str_input)

        self.client.post(
            '/blog/create_post/',
            {
                'title': 'Post Form 만들기',
                'content': 'Post Form 페이지를 만듭시다.',
                'tags_str': 'new tag; test tag, Python',
            }
        )
        last_post = Post.objects.last()
        self.assertEqual(last_post.title, "Post Form 만들기")
        self.assertEqual(last_post.author.username, 'obama')

        self.assertEqual(last_post.tags.count(), 3)
        self.assertTrue(Tag.objects.get(name='new tag'))
        self.assertTrue(Tag.objects.get(name='test tag'))
        self.assertTrue(Tag.objects.get(name='Python'))
        self.assertEqual(Tag.objects.count(), 5)

    def test_update_post(self):
        update_post_url = f'/blog/update_post/{self.post_003.pk}/'

        # 로그인을 하지 않은 경우에는 update_post_url로 접근했을 때 status_code가 200이 나오면 안된다.
        response = self.client.get(update_post_url)
        self.assertNotEqual(response.status_code, 200)

        # 로그인을 했지만 작성자가 아닌 경우에는 status_code가 403이 나와야 한다.
        self.assertNotEqual(self.post_003.author, self.user_trump)
        self.client.login(
            username=self.user_trump,
            password='somepassword'
        )
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 403)

        # 작성자가 접근하는 경우
        self.client.login(
            username=self.user_obama,
            password='somepassword'
        )
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Edit Post - Blog', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Edit Post', main_area.text)

        tag_str_input = main_area.find('input', id='id_tags_str')
        self.assertTrue(tag_str_input)
        self.assertIn('python_kor; Python', tag_str_input.attrs['value'])

        response = self.client.post(
            update_post_url,
            {
                'title': '3rd post updated',
                'content': 'Hi, We are the one',
                'category': self.category_music.pk,
                'tags_str': 'python_kor; test tag, some tag',
            },
            follow=True
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn('3rd post updated', main_area.text)
        self.assertIn('Hi, We are the one', main_area.text)
        self.assertIn(self.category_music.name, main_area.text)
        self.assertIn('python_kor', main_area.text)
        self.assertIn('test tag', main_area.text)
        self.assertIn('some tag', main_area.text)
        self.assertNotIn('Python', main_area.text)

    def test_comment_form(self):
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.post_001.comment_set.count(), 1)

        # Not login
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('div', id='comment-area')
        self.assertIn('Log in and leave a comment', comment_area.text)
        self.assertFalse(comment_area.find('form', id='comment-form'))

        # login
        self.client.login(username='obama', password='somepassword')
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('div', id='comment-area')
        self.assertNotIn('Log in and leave a comment', comment_area.text)

        comment_form = comment_area.find('form', id='comment-form')
        self.assertTrue(comment_form.find('textarea', id='id_content'))
        response = self.client.post(
            self.post_001.get_absolute_url() + 'new_comment/',
            {
                'content': "This is comment made by obama",
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(self.post_001.comment_set.count(), 2)

        new_comment = Comment.objects.last()

        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIn(new_comment.post.title, soup.title.text)

        comment_area = soup.find('div', id='comment-area')
        new_comment_div = comment_area.find('div', id=f'comment-{new_comment.pk}')
        self.assertIn('obama', new_comment_div.text)
        self.assertIn('This is comment made by obama', new_comment_div.text)


    def test_comment_update(self):
        comment_by_trump = Comment.objects.create(
            post=self.post_001,
            author=self.user_trump,
            content='This is comment made by trump',
        )
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('div', id='comment-area')
        self.assertFalse(comment_area.find('a', id='comment-1-update-btn'))
        self.assertFalse(comment_area.find('a', id='comment-2-update-btn'))

        # login
        self.client.login(username='obama', password='somepassword')
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('div', id='comment-area')
        self.assertFalse(comment_area.find('a', id='comment-2-update-btn'))
        comment_001_update_btn = comment_area.find('a', id='comment-1-update-bin')
        self.assertIn('edit', comment_001_update_btn.text)
        self.assertEqual(comment_001_update_btn.attrs['href'], '/blog/update_comment/1/')

        response = self.client.get('/blog/update_comment/1/')
        self.assertEqual(response.status_code, 200)
        soup =BeautifulSoup(response.contentm 'html.parser')

        self.assertEqual('Edit Comment - Blog', soup.title.text)
        update_comment_form = soup.find('form', id='comment-form')
        content_textarea = update_comment_form.find('textarea', id='id_content')
        self.assertIn(self.comment_001.content, content_textarea.text)

        response = self.client.post(
            f'/blog/update_comment/{self.comment_001.pk}/',
            {
                'content': "Edit obama comment",
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        comment_001_div = soup.find('div', id='comment-1')
        self.assertIn('Edit obama comment', comment_001_div.text)
        self.assertIn('Updated: ', comment_001_div.text)

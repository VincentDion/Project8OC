import time

from django.test import TestCase, Client
from django.urls import reverse

from django.contrib.auth.models import User

from .models import Product, UserFavorite
from .forms import UserRegisterForm, ChangeMailForm

# We try to have a pattern in test cases such as we always test for each page that :
#   - The right template is used
#   - The path is correct according to the urls files
#   - Elements from context are right
#   - Status code is right (200, 302 or 404)

# Other kind of tests focus on testing a specific function, or user permissions and such

# SetUp for tests are made for each page, although quite similars, improvements coming in future versions

class IndexPageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('bestproduct:index'))
        self.assertTemplateUsed(response, 'bestproduct/base.html')
        self.assertTemplateUsed(response, 'bestproduct/index.html')
        self.assertEqual(response.request.get('PATH_INFO'), "/")
        self.assertEqual(response.status_code, 200)
        

class LegalNoticePageTestCase(TestCase):
    def test_legal_notice_page(self):
        response = self.client.get(reverse('besproduct:legal_notice'))
        self.assertTemplateUsed(response, 'bestproduct/base.html')
        self.assertTemplateUsed(response, 'bestproduct/legal_notice.html')
        self.assertEqual(response.request.get('PATH_INFO'), "/legal_notice/")
        self.assertEqual(response.status_code, 200)


class DetailPageTestCase(TestCase):

    def setUp(self):
        Product.objects.all().delete()
        Product.objects.create(name="test_item",
                               category="test_category",
                               nutrition_grade="a",
                               picture="https://static.djangoproject.com/img/logos/django-logo-negative.png")
        self.product = Product.objects.get(name="test_item")

    def test_detail_page(self):
        product_id = self.product.id
        response = self.client.get(reverse('bestproduct:detail', args=(product_id,)))

        self.assertEqual(response.context['image'], "https://static.djangoproject.com/img/logos/django-logo-negative.png")
        self.assertEqual(response.context['name'], "test_item")
        self.assertEqual(response.context['product'], Product.objects.get(name="test_item"))

        self.assertEqual(response.request.get('PATH_INFO'), "/detail/%s/" % (product_id))

        self.assertTemplateUsed(response, 'bestproduct/base.html')
        self.assertTemplateUsed(response, 'bestproduct/detail.html')

        self.assertEqual(response.status_code, 200)

    def test_detail_page_returns_404_if_product_not_in_db(self):
        product_id = self.product.id + 1
        response = self.client.get(reverse('bestproduct:detail', args=(product_id,)))
        self.assertEqual(response.request.get('PATH_INFO'), "/detail/%s/" % (product_id))
        self.assertEqual(response.status_code, 404)


# Documentation : https://docs.djangoproject.com/fr/2.2/topics/testing/tools/
class LoginPageTestCase(TestCase):
    # Tests to verify if logging works is done for each page that required logging
    def setUp(self):
        User.objects.all().delete()
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_login_page(self):
        response = self.client.get(reverse('besproduct:login'))

        self.assertEqual(response.request.get('PATH_INFO'), "/login/")

        self.assertTemplateUsed(response, 'bestproduct/base.html')
        self.assertTemplateUsed(response, 'bestproduct/login.html')

        self.assertEqual(response.status_code, 200)

    def test_login_works_with_right_credentials(self):
        c = Client()
        response = c.post('/login/', {'username': 'john', 'password': 'johnpassword'}, follow=True)
        self.assertEqual(response.redirect_chain[0][-1], 302)
        self.assertEqual(response.redirect_chain[0][0], '/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bestproduct/index.html')

    def test_login_page_reload_with_wrong_credentials(self):
        # Entering wrong credentials lead the user to reload the loading page
        c = Client()
        response = c.post('/login/', {'username': 'john', 'password': 'covfefe'}, follow=True)
        self.assertEqual(response.redirect_chain, [])
        self.assertEqual(response.request.get('PATH_INFO'), "/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bestproduct/login.html')

    def test_user_logging_with_wrong_credential_is_indeed_not_logged_in(self):
        c = Client()
        response = c.post('/login/', {'username': 'john', 'password': 'covfefe'})
        response = self.client.get(reverse('bestproduct:profile'), follow=True)

        # We verify the user can't access the logged only page and is indeed redirected to the login page
        self.assertEqual(response.redirect_chain[0][-1], 302)
        self.assertEqual(response.redirect_chain[0][0], '/login?next=/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bestproduct/login.html')

class LogoutTestCase(TestCase):
    def setUp(self):
        User.objects.all().delete()
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_logout(self):
        c = Client()
        response = c.post('/login/', {'username': 'john', 'password': 'johnpassword'})
        response = c.get('/logout/', follow=True)

        # Test of redirect chain, we must have a redirection first, to the url '/', from which we have a 200
        # Last one is to test we're indeed on the index page (TO BE IMPROVED - need to know how to test current url)
        self.assertEqual(response.redirect_chain[0][-1], 302)
        self.assertEqual(response.redirect_chain[0][0], '/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bestproduct/index.html')
        

    def test_logged_out_user_can_not_access_page_that_require_login(self):
        c = Client()

        # User log in, then log out, then try to access a logged only page
        response = c.post('/login/', {'username': 'john', 'password': 'johnpassword'})
        response = c.get('/logout/')
        response = self.client.get(reverse('bestproduct:profile'), follow=True)

        # We verify the user can't access the logged only page and is indeed redirected to the login page
        self.assertEqual(response.redirect_chain[0][-1], 302)
        self.assertEqual(response.redirect_chain[0][0], '/login?next=/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bestproduct/login.html')


class ProfilePageTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_profile_page_is_not_accessible_for_user_not_logged_in(self):
        response = self.client.get(reverse('bestproduct:profile'), follow=True)
        self.assertEqual(response.redirect_chain[0][-1], 302)
        self.assertEqual(response.redirect_chain[0][0], '/login?next=/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bestproduct/login.html')

    def test_profile_page_is_accessible_and_with_right_informations_if_connected(self):
        c = Client()
        response = c.post('/login/', {'username': 'john', 'password': 'johnpassword'})
        response = c.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bestproduct/base.html')
        self.assertTemplateUsed(response, 'bestproduct/profile.html')
        self.assertEqual(response.context['email'], 'lennon@thebeatles.com')


class ReplacePageTestCase(TestCase):
    def setUp(self):
        """ 
        We create 5 items :
            - 4 items from the same category, with different nutrition grades
            - 1 item with the best grade but from a different category
        """
        Product.objects.all().delete()
        Product.objects.create(name="item_1",
                               category="category_1",
                               brand="brand_1",
                               nutrition_grade="b",
                               picture="https://test.com/img_item_1.png",
                               nutrition_image="https://test.com/img_grade_b.png",
                               url="https://test.com/item_1")

        Product.objects.create(name="item_2",
                               category="category_1",
                               brand="brand_2",
                               nutrition_grade="c",
                               picture="https://test.com/img_item_2.png",
                               nutrition_image="https://test.com/img_grade_c.png",
                               url="https://test.com/item_2")

        Product.objects.create(name="item_3",
                               category="category_1",
                               brand="brand_3",
                               nutrition_grade="a",
                               picture="https://test.com/img_item_3.png",
                               nutrition_image="https://test.com/img_grade_a.png",
                               url="https://test.com/item_3")

        Product.objects.create(name="item_4",
                               category="category_1",
                               brand="brand_4",
                               nutrition_grade="c",
                               picture="https://test.com/img_item_4.png",
                               nutrition_image="https://test.com/img_grade_c.png",
                               url="https://test.com/item_4")

        Product.objects.create(name="item_5",
                               category="category_2",
                               brand="brand_5",
                               nutrition_grade="a",
                               picture="https://test.com/img_item_5.png",
                               nutrition_image="https://test.com/img_grade_a.png",
                               url="https://test.com/item_5")


    def test_replace_page_with_item_1_as_query(self):
        c = Client()
        response = c.get('/replace/', {'query': 'item_1'})

        # Since item_1 is in db, we must have a 200 to replace page, with item_1 image and name on banner
        # Rest of tests from items within db won't test that in particualr, as it follows same pattern
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bestproduct/base.html')
        self.assertTemplateUsed(response, 'bestproduct/replace.html')
        self.assertEqual(response.context['image'], "https://test.com/img_item_1.png")
        self.assertEqual(response.context['name'], "item_1")

        # Only item 3 is suitable as replacement, so only its information have to be send in context
        self.assertEqual(len(response.context['substitutes']), 1)
        self.assertEqual(response.context['substitutes'][0], Product.objects.get(name='item_3'))
        self.assertEqual(response.context['substitutes'][0].name, 'item_3')
        self.assertEqual(response.context['substitutes'][0].nutrition_image, 'https://test.com/img_grade_a.png')
        self.assertEqual(response.context['substitutes'][0].picture, 'https://test.com/img_item_3.png')


    def test_replace_page_with_item_2_as_query(self):
        c = Client()
        response = c.get('/replace/', {'query': 'item_2'})

        # items 1 & 3 are suitables as replacements, but 3 must comes first in the list, since its grade is 'a'
        self.assertEqual(len(response.context['substitutes']), 2)
        self.assertEqual(response.context['substitutes'][0], Product.objects.get(name='item_3'))
        self.assertEqual(response.context['substitutes'][0].name, 'item_3')
        self.assertEqual(response.context['substitutes'][0].nutrition_image, 'https://test.com/img_grade_a.png')
        self.assertEqual(response.context['substitutes'][0].picture, 'https://test.com/img_item_3.png')
        self.assertEqual(response.context['substitutes'][1], Product.objects.get(name='item_1'))
        self.assertEqual(response.context['substitutes'][1].name, 'item_1')
        self.assertEqual(response.context['substitutes'][1].nutrition_image, 'https://test.com/img_grade_b.png')
        self.assertEqual(response.context['substitutes'][1].picture, 'https://test.com/img_item_1.png')


    def test_replace_page_with_item_3_as_query(self):
        c = Client()
        response = c.get('/replace/', {'query': 'item_3'})

        # No item is suitable as replacement, page must be empty
        self.assertEqual(len(response.context['substitutes']), 0)

    # We do not need to test items 4 & 5

    def test_replace_function_if_product_does_not_exist(self):
        # User must be redirected to main page
        c = Client()
        response = c.get('/replace/', {'query': 'jus'}, follow=True)
        self.assertEqual(response.redirect_chain[0][-1], 302)
        self.assertEqual(response.redirect_chain[0][0], '/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bestproduct/index.html')



class RegisterPageTestCase(TestCase):
    def setUp(self):
        # Cleanse of DB to test on a fresh one
        User.objects.all().delete()
        User.objects.create_user('paul', 'paul@thebeatles.com', 'paulpassword')

    def test_register_page(self):
        
        # We call the form to be test in the context
        form = UserRegisterForm()
        response = self.client.get(reverse('besproduct:register'))

        self.assertEqual(response.request.get('PATH_INFO'), "/register/")

        self.assertTemplateUsed(response, 'bestproduct/base.html')
        self.assertTemplateUsed(response, 'bestproduct/register.html')

        self.assertEqual(type(response.context['form']), type(form))
        
        self.assertEqual(response.status_code, 200)

    def test_register_page_redirects_to_login_if_valid_form(self):
        c = Client()
        response = c.post('/register/', {'username': 'john', 'email': 'lennon@thebeatles.com',
                          'password1': 'johnpassword', 'password2': 'johnpassword'}, follow=True)
        self.assertEqual(response.redirect_chain[0][-1], 302)
        self.assertEqual(response.redirect_chain[0][0], '/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bestproduct/login.html')

        # We test that the user is indeed added in the database
        user = User.objects.get(username="john")
        self.assertEqual(user.email, 'lennon@thebeatles.com')

    def test_register_page_reloads_if_not_same_pwd(self):
        c = Client()
        response = c.post('/register/', {'username': 'john', 'email': 'lennon@thebeatles.com',
                          'password1': 'johnpassword', 'password2': 'other'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bestproduct/register.html')

        # We test that number of users in db is still 1 (from SetUp)
        users = User.objects.all()
        self.assertEqual(len(users), 1)

    def test_register_page_reloads_if_not_valid_mail(self):
        c = Client()
        response = c.post('/register/', {'username': 'john', 'email': 'lennon', 'password1': 'johnpassword', 'password2': 'johnpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bestproduct/register.html')

        # We test that number of users in db is still 1 (from SetUp)
        users = User.objects.all()
        self.assertEqual(len(users), 1)

    def test_register_page_reloads_if_user_already_exists(self):
        c = Client()
        response = c.post('/register/', {'username': 'paul', 'email': 'john@thebeatles.com', 'password1': 'johnpassword', 'password2': 'johnpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bestproduct/register.html')

        # We test that number of users in db is still 1 (from SetUp)
        users = User.objects.all()
        self.assertEqual(len(users), 1)


class FavoritePageTestCase(TestCase):
    """ 
    Class to test Favorite page and both del and add favorites function, 
    although only the del is accessible from the favorite page.
    """
    def setUp(self):
        """
        For this set of tests, we create 2 users and 3 products :
            - User 'john' has already item_2 in its favorite and we will test with him adding/deleting favorites
            - User 'paul' has item_1 & items_3 in its favorites
        """
        Product.objects.all().delete()
        User.objects.all().delete()
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        User.objects.create_user('paul', 'paul@thebeatles.com', 'paulpassword')
        u = User.objects.get(username='john')

        Product.objects.create(name="item_1",
                               category="category_1",
                               brand="brand_1",
                               nutrition_grade="b",
                               picture="https://test.com/img_item_1.png",
                               nutrition_image="https://test.com/img_grade_b.png",
                               url="https://test.com/item_1")
        Product.objects.create(name="item_2",
                               category="category_1",
                               brand="brand_2",
                               nutrition_grade="a",
                               picture="https://test.com/img_item_2.png",
                               nutrition_image="https://test.com/img_grade_a.png",
                               url="https://test.com/item_2")
        Product.objects.create(name="item_3",
                               category="category_1",
                               brand="brand_3",
                               nutrition_grade="a",
                               picture="https://test.com/img_item_3.png",
                               nutrition_image="https://test.com/img_grade_a.png",
                               url="https://test.com/item_3")
        p = Product.objects.get(name="item_2")

        # We add item_2 as a favorite of 'john'
        uf = UserFavorite(user_name=u, product=p)
        uf.save()

        # We add item_1 and 3 as a favorite of 'paul'
        u = User.objects.get(username='paul')
        p = Product.objects.get(name="item_1")
        uf = UserFavorite(user_name=u, product=p)
        uf.save()
        p = Product.objects.get(name="item_3")
        uf = UserFavorite(user_name=u, product=p)
        uf.save()


    def test_setUp_is_successfull(self):
        # Test that DB has two users, 3 products and 3 entries in favorites total
        number_of_user = User.objects.all()
        number_of_products = Product.objects.all()
        fav_list = UserFavorite.objects.all()

        self.assertEqual(len(number_of_user), 2)
        self.assertEqual(len(number_of_products), 3)
        self.assertEqual(len(fav_list), 3)

        # We test 'john' has the right number of favorite
        user_id = User.objects.get(username='john')
        favorite_list = Product.objects.filter(userfavorite__user_name=user_id.id)
        self.assertEqual(len(favorite_list), 1)
        self.assertEqual(favorite_list[0], Product.objects.get(name="item_2"))

        # We test 'paul' has the right number of favorite
        user_id = User.objects.get(username='paul')
        favorite_list = Product.objects.filter(userfavorite__user_name=user_id.id)
        self.assertEqual(len(favorite_list), 2)


    def test_favorite_page_accessible_and_with_right_informations_if_connected(self):
        c = Client()
        response = c.post('/login/', {'username': 'john', 'password': 'johnpassword'})
        response = c.get('/favorite/')

        self.assertEqual(response.request.get('PATH_INFO'), "/favorite/")

        self.assertTemplateUsed(response, 'bestproduct/base.html')
        self.assertTemplateUsed(response, 'bestproduct/favorite.html')

        # We test favorite page contains the one good favorite from setUp
        self.assertEqual(len(response.context['favorites']), 1)
        self.assertEqual(response.context['favorites'][0], Product.objects.get(name='item_2'))
        
        self.assertEqual(response.status_code, 200)

    def test_favorite_page_redirects_to_login_if_not_connected(self):
        c = Client()
        response = c.get('/favorite/', follow=True)
        self.assertEqual(response.redirect_chain[0][-1], 302)
        self.assertEqual(response.redirect_chain[0][0], '/login?next=/favorite/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bestproduct/login.html')
    

    def test_del_favorite(self):
        product = Product.objects.get(name="item_2")
        self.client.login(username= 'john', password= 'johnpassword')
        self.client.get(reverse('bestproduct:favorite'))

        response = self.client.post(reverse('bestproduct:del_favorite', args=str(product.id)), follow=True)

        user_id = User.objects.get(username='john')
        favorite_list = Product.objects.filter(userfavorite__user_name=user_id.id)
        self.assertEqual(len(favorite_list), 0)
        self.assertEqual(response.redirect_chain[0][-1], 302)
        self.assertEqual(response.redirect_chain[0][0], '/favorite/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bestproduct/favorite.html')

    def test_del_favorite_with_wrong_id_reloads_favorite(self):
        product = Product.objects.get(name="item_3")
        self.client.login(username= 'john', password= 'johnpassword')
        self.client.get(reverse('bestproduct:favorite'))

        response = self.client.post(reverse('bestproduct:del_favorite', args=str(product.id)), follow=True)

        user_id = User.objects.get(username='john')
        favorite_list = Product.objects.filter(userfavorite__user_name=user_id.id)
        self.assertEqual(len(favorite_list), 1)
        self.assertEqual(response.redirect_chain[0][-1], 302)
        self.assertEqual(response.redirect_chain[0][0], '/favorite/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bestproduct/favorite.html')

    """
    #This test is commented while working on a fix caused by the redirect in view
    def test_add_favorite(self):       
        product = Product.objects.get(name="item_3")
        self.client.login(username= 'john', password= 'johnpassword')
        self.client.get(reverse('bestproduct:replace'), {'query':'item_1'})

        response = self.client.post(reverse('bestproduct:add_favorite', args=str(product.id)), follow=True)

        user_id = User.objects.get(username='john')
        favorite_list = Product.objects.filter(userfavorite__user_name=user_id.id)
        self.assertEqual(len(favorite_list), 2)
    """

class MailChangePageTestCase(TestCase):
    def setUp(self):
        User.objects.all().delete()
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_user_redirected_to_login_if_not_connected(self):
        c = Client()
        response = c.get('/mail_change/', follow=True)
        self.assertEqual(response.redirect_chain[0][-1], 302)
        self.assertEqual(response.redirect_chain[0][0], '/login?next=/mail_change/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bestproduct/login.html')

    def test_mail_change_page_accessible_if_connected(self):
        form = ChangeMailForm()
        c = Client()
        response = c.post('/login/', {'username': 'john', 'password': 'johnpassword'})
        response = c.get('/mail_change/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bestproduct/base.html')
        self.assertTemplateUsed(response, 'bestproduct/mail_change.html')
        self.assertEqual(response.request.get('PATH_INFO'), "/mail_change/")
        self.assertEqual(type(response.context['form']), type(form))

    def test_mail_change_function_change_user_mail(self):
        # Test user's mail is indeed changed and he is redirected to his profile
        c = Client()
        response = c.post('/login/', {'username': 'john', 'password': 'johnpassword'})
        response = c.post('/mail_change/', {'email' : 'lennon@johnyoko.com'}, follow=True)

        user = User.objects.get(username="john")
        self.assertEqual(user.email, 'lennon@johnyoko.com')
        self.assertEqual(response.redirect_chain[0][-1], 302)
        self.assertEqual(response.redirect_chain[0][0], '/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bestproduct/profile.html')

    def test_mail_change_fonction_reload_with_non_valid_mail(self):
        c = Client()
        response = c.post('/login/', {'username': 'john', 'password': 'johnpassword'})
        response = c.post('/mail_change/', {'email' : 'jonh&yoko'}, follow=True)

        # We test mail has not change too
        user = User.objects.get(username="john")
        self.assertEqual(user.email, 'lennon@thebeatles.com')

        self.assertEqual(response.request.get('PATH_INFO'), "/mail_change/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bestproduct/mail_change.html')


# Documentation for new tests :
    # http://www.test-recette.fr/tests-techniques/deployer-tests-integration/tests-integration-django.html
    # class response : https://docs.djangoproject.com/fr/3.0/topics/testing/tools/
    # test login : https://stackoverflow.com/questions/7367509/login-in-django-testing-framework
    # URLField : http://www.learningaboutelectronics.com/Articles/How-to-create-a-URLField-in-Django.php
    # test type : https://stackoverflow.com/questions/33657463/python-test-to-check-instance-type/33657828
    # https://docs.djangoproject.com/fr/2.2/_modules/django/test/utils/
    # https://stackoverflow.com/questions/14951356/django-testing-if-the-page-has-redirected-to-the-desired-url
    # https://docs.djangoproject.com/fr/3.0/topics/http/urls/
    # Test coverage : https://pypi.org/project/django-nose/
    # https://stackoverflow.com/questions/53461410/make-user-email-unique-django/53461823
    # https://docs.djangoproject.com/fr/3.0/ref/request-response/
    # https://stackoverflow.com/questions/50114484/django-why-is-my-form-sending-post-data-but-returning-request-method-get
    # https://stackoverflow.com/questions/40750803/django-test-request-method-post-not-working
    # https://stackoverflow.com/questions/44726762/django-test-client-client-post-sends-get-request
    # https://docs.djangoproject.com/en/3.0/topics/forms/#the-view
    # https://medium.com/@fro_g/making-post-requests-work-with-django-tests-3d9ad539e11f
    # https://stackoverflow.com/questions/2619102/djangos-self-client-login-does-not-work-in-unit-tests
    # https://www.pythoncircle.com/post/424/solving-django-error-noreversematch-at-url-with-arguments-and-keyword-arguments-not-found/
    # https://docs.djangoproject.com/fr/3.0/ref/request-response/

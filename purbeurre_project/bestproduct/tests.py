from django.test import TestCase, Client
from django.urls import reverse

from django.contrib.auth.models import User

from .models import Product, UserFavorite


class IndexPageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('bestproduct:index'))
        self.assertEqual(response.status_code, 200)


class LegalNoticePageTestCase(TestCase):
    def test_legal_notice_page(self):
        response = self.client.get(reverse('besproduct:legal_notice'))
        self.assertEqual(response.status_code, 200)


class DetailPageTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="produit impossible")
        self.product = Product.objects.get(name="produit impossible")

    def test_detail_page_returns_200(self):
        product_id = self.product.id
        response = self.client.get(reverse('bestproduct:detail', args=(product_id,)))
        self.assertEqual(response.status_code, 200)

    def test_detail_page_returns_404(self):
        product_id = self.product.id + 1
        response = self.client.get(reverse('bestproduct:detail', args=(product_id,)))
        self.assertEqual(response.status_code, 404)


# Documentation : https://docs.djangoproject.com/fr/2.2/topics/testing/tools/
class LoginPageTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_login_page(self):
        response = self.client.get(reverse('besproduct:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_returns_302_if_right_logins(self):
        # Returns 302 because user is redirected to main page
        c = Client()
        response = c.post('/login/', {'username': 'john', 'password': 'johnpassword'})
        self.assertEqual(response.status_code, 302)

    def test_login_page_returns_200_if_wrong_logins(self):
        # Returns 200 because the same page is reloaded
        c = Client()
        response = c.post('/login/', {'username': 'john', 'password': 'veverv'})
        self.assertEqual(response.status_code, 200)


class ProfilePageTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_profile_page_returns_302_if_not_connected(self):
        # 302 because redirected and end up on 404 page
        response = self.client.get(reverse('bestproduct:profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_page_returns_200_if_connected(self):
        # Simulation of user connexion before accessing profile page
        c = Client()
        response = c.post('/login/', {'username': 'john', 'password': 'johnpassword'})
        response = c.get('/profile/')
        self.assertEqual(response.status_code, 200)


class ReplacePageTestCase(TestCase):
    def setUp(self):
        # Cleanse of DB to test on a fresh one
        Product.objects.all().delete()
        Product.objects.create(name="impossible")

    def test_replace_page_returns_200_if_product_exists(self):
        c = Client()
        response = c.get('/replace/', {'query': 'impossible'})
        self.assertEqual(response.status_code, 200)

    def test_replace_page_returns_302_if_product_does_not_exist(self):
        # 302 because user is redirected to actual page with a warning
        c = Client()
        response = c.get('/replace/', {'query': 'jus'})
        self.assertEqual(response.status_code, 302)


class RegisterPageTestCase(TestCase):
    def setUp(self):
        # Cleanse of DB to test on a fresh one
        User.objects.all().delete()
        User.objects.create_user('paul', 'paul@thebeatles.com', 'paulpassword')

    def test_register_page(self):
        response = self.client.get(reverse('besproduct:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_page_returns_302_if_valid(self):
        c = Client()
        response = c.post('/register/', {'username': 'john', 'email': 'lennon@thebeatles.com', 'password1': 'johnpassword', 'password2': 'johnpassword'})
        self.assertEqual(response.status_code, 302)

    def test_register_page_returns_200_if_not_same_pwd(self):
        c = Client()
        response = c.post('/register/', {'username': 'john', 'email': 'lennon@thebeatles.com', 'password1': 'johnpassword', 'password2': 'other'})
        self.assertEqual(response.status_code, 200)

    def test_register_page_returns_200_if_not_valid_mail(self):
        c = Client()
        response = c.post('/register/', {'username': 'john', 'email': 'lennon', 'password1': 'johnpassword', 'password2': 'johnpassword'})
        self.assertEqual(response.status_code, 200)

    def test_register_page_returns_200_if_user_already_exists(self):
        c = Client()
        response = c.post('/register/', {'username': 'paul', 'email': 'john@thebeatles.com', 'password1': 'johnpassword', 'password2': 'johnpassword'})
        self.assertEqual(response.status_code, 200)

    def test_register_success_create_new_user_in_db(self):
        c = Client()
        c.post('/register/', {'username': 'john', 'email': 'lennon@thebeatles.com', 'password1': 'johnpassword', 'password2': 'johnpassword'})
        user = User.objects.get(username="john")
        self.assertEqual(user.username, "john")


class FavoritePageTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_favorite_page_returns_200_if_connected(self):
        c = Client()
        response = c.post('/login/', {'username': 'john', 'password': 'johnpassword'})
        response = c.get('/favorite/')
        self.assertEqual(response.status_code, 200)

    def test_favorite_page_returns_302_if_not_connected(self):
        c = Client()
        response = c.get('/favorite/')
        self.assertEqual(response.status_code, 302)


# add favorite function
    # test that a new favorite is indeed added to the DB
    # test that a favorite already in the DB can't be added twice

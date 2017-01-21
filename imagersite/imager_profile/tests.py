"""Tests for the lender_profile app."""
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
import factory

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "The Chosen {}".format(n))
    email = factory.LazyAttribute(
        lambda x: "{}@foo.com".format(x.username.replace(" ", ""))
    )


class ProfileTestCase(TestCase):
    """The Profile Model test runner."""

    def setUp(self):
        """The appropriate setup for the appropriate test."""
        self.users = [UserFactory.create() for i in range(20)]

    def test_profile_is_made_when_user_is_saved(self):
        """Imager Profile should be created when a User is saved."""
        self.assertTrue(ImagerProfile.objects.count() == 20)

    def test_profile_is_associated_with_actual_users(self):
        """Imager Profile should be attached to User."""
        profile = ImagerProfile.objects.first()
        self.assertTrue(hasattr(profile, "user"))
        self.assertIsInstance(profile.user, User)

    def test_user_has_profile_attached(self):
        """User should have a Imager Profile attached."""
        user = self.users[0]
        self.assertTrue(hasattr(user, "profile"))
        self.assertIsInstance(user.profile, ImagerProfile)

    def test_user_is_active(self):
        """User should be active."""
        user = self.users[0]
        self.assertTrue(user.is_active)
        self.assertTrue(user.profile.is_active)

    def test_str_method_on_imager_profile(self):
        """String method should return a string."""
        user = self.users[0]
        self.assertTrue(type(str(user.profile)), str)
        self.assertTrue(str(user.profile) == 'Username: {}\n                  Camera: \n                  Photography Type: \n                  Employable?: True\n                  Address: None\n                  About Me: \n                  Website: None\n                  Phone: None\n                  Travel Radius: None'.format(user.username))

    def test_inactive_users(self):
        """Test that inactive users are not active."""
        the_user = self.users[0]
        the_user.is_active = False
        the_user.save()
        self.assertTrue(ImagerProfile.active.count() == User.objects.count() - 1)


class ProfileFrontEndTests(TestCase):
    """Tests for the imager profile front end."""

    def setUp(self):
        self.client = Client()
        self.request = RequestFactory()

    def register_new_user(self, follow=True):
        return self.client.post("/registration/register/", {
            "username": "Jerry",
            "email": "jerry@reed.com",
            "password1": "tugboats",
            "password2": "tugboats"
        }, follow=follow)

    def test_home_view_is_status_ok(self):
        """Test a get request on the home_page view."""
        from imagersite.views import home_page
        req = self.request.get("/potato")
        response = home_page(req)
        self.assertTrue(response.status_code == 200)

    def test_home_route_is_status_ok(self):
        """Test a 200 response on the home route."""
        response = self.client.get("/")
        self.assertTrue(response.status_code == 200)

    def test_home_route_uses_correct_templates(self):
        """Test that the correct templates are used on the home page."""
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")
        self.assertTemplateUsed(response, "base.html")

    def test_login_route_is_status_ok(self):
        """Test for a 200 status route at /login."""
        response = self.client.get("/login/")
        self.assertTrue(response.status_code == 200)

    def test_login_route_redirects(self):
        """Login route redirect?."""
        new_user = UserFactory.create()
        new_user.set_password("tugboats")
        new_user.save()
        response = self.client.post("/login/", {
            "username": new_user.username,
            "password": "tugboats"
        }, follow=False)
        self.assertTrue(response.status_code == 302)

    def test_login_route_redirects_to_home(self):
        """Login route redirect to homepage?."""
        new_user = UserFactory.create()
        new_user.set_password("tugboats")
        new_user.save()
        response = self.client.post("/login/", {
            "username": new_user.username,
            "password": "tugboats"}, follow=True)
        self.assertTrue(response.redirect_chain[0][0] == '/')

    def test_register_new_user(self):
        """Test a new user is created."""
        self.assertTrue(User.objects.count() == 0)
        self.register_new_user()
        self.assertTrue(User.objects.count() == 1)

    def test_registered_user_is_not_active(self):
        """Test a newly registered user is inactive."""
        self.register_new_user()
        the_user = User.objects.first()
        self.assertFalse(the_user.is_active)

    def test_registered_user_redirects(self):
        """Test registration redirects."""
        response = self.register_new_user(follow=False)
        self.assertTrue(response.status_code == 302)

    def test_registered_user_redirects_home(self):
        """Test registration redirects to proper location."""
        response = self.register_new_user(follow=True)
        self.assertTrue(response.redirect_chain[0][0] == '/registration/register/complete/')

    def test_logout_route_redirects_to_home(self):
        """Logout route redirect to homepage?."""
        new_user = UserFactory.create()
        new_user.set_password("tugboats")
        new_user.save()
        self.client.post("/login/", {
            "username": new_user.username,
            "password": "tugboats"}, follow=True)
        response = self.client.get("/logout/", follow=True)
        self.assertTrue(response.redirect_chain[0][0] == '/')

    def test_logout_route_redirects(self):
        """Logout route redirect in general?."""
        new_user = UserFactory.create()
        new_user.set_password("tugboats")
        new_user.save()
        self.client.post("/login/", {
            "username": new_user.username,
            "password": "tugboats"}, follow=True)
        response = self.client.get("/logout/")
        self.assertTrue(response.status_code == 302)
from django.test import TestCase, Client
from django.contrib.auth.models import User

# Create your tests here.

# Try random combinations of filters
class MailerTest(TestCase):
	def setUp(self):
		self.client = Client()
		self.password = 'password'
		self.my_admin = User.objects.create_superuser('test', 'test@test.edu', self.password)

	def test_page(self):
		# should be unable to access the mailer page without logging in
		response = self.client.get('/api/mailer')
		self.assertEqual(response.status_code, 302)

		# verify login
		login = self.client.login(username=self.my_admin.username, password=self.password)
		self.assertEqual(login, True)

		# now access mailer
		response = self.client.get('/api/mailer', follow=True)
		self.assertEqual(response.status_code, 200)
		
		self.client.logout()





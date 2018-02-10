import os
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.models import ImageField, FileField, URLField, TextField
from django.core.files import File

# Create your tests here.
from portfolio_api.models import User

class UserModelTest(TestCase):
	""" This class defines the test suite for the custom User model """
	@classmethod
	def setUpTestData(self):
		# set up data and variables available for all test methods
		# a user with all required fields set
		self.valid_user = User.objects.create(username='geek', password='password', first_name='Geek', last_name='User', email='geek@example.com')
		self.current_dir = os.path.dirname(os.path.abspath(__file__))

	def setUp(self):
		# runs before all test methods, with clean data
		self.user = User.objects.create(username='nerd', password='password')

	def test_first_name_is_required(self):
		# The modified User model must require first name
		self.user.email='nerd@example.com'
		self.user.last_name = 'User'
		with self.assertRaises(ValidationError):
			self.user.save()
			self.user.full_clean()

	def test_last_name_is_required(self):
		# The modified User model must require last name
		self.user.email='nerd@example.com'
		self.user.first_name = 'Nerd'
		with self.assertRaises(ValidationError):
			self.user.save()
			self.user.full_clean()

	def test_email_is_required(self):
		# The modified User model must require first name
		self.user.first_name="Nerd"
		self.user.last_name = 'User'
		with self.assertRaises(ValidationError):
			self.user.save()
			self.user.full_clean()

	def test_short_bio_field_exists_with_correct_max_lenght(self):
		field = self.user._meta.get_field('short_bio')
		self.assertTrue(isinstance(field, TextField))
		max_length = self.user._meta.get_field('short_bio').max_length
		self.assertEquals(max_length, 300)

	def test_image_field_exists_and_saves_image_correctly(self):
		field = self.user._meta.get_field('image')
		self.assertTrue(isinstance(field, ImageField))
		img = File(open(os.path.join(self.current_dir, 'test.jpg'), 'rb'))
		self.valid_user.image = img
		self.valid_user.save()
		
		# file will be saved in a subdirectory of media named after the user id
		self.assertIn("uploads/user_{0!s}/test.jpg".format(self.valid_user.id), self.valid_user.image.path)
		
		# close file and delete the uploaded file
		img.close
		self.valid_user.image.delete(save=True)

	def test_resume_field_exists(self):
		field = self.user._meta.get_field('resume')
		self.assertTrue(isinstance(field, FileField))
		resume = File(open(os.path.join(self.current_dir, 'test.doc'), 'rb'))
		self.valid_user.resume = resume
		self.valid_user.save()
		
		# file will be saved in a subdirectory of media named after the user id
		self.assertIn("uploads/user_{0!s}/test.doc".format(self.valid_user.id), self.valid_user.resume.path)
		
		# close file and delete uploaded file
		resume.close
		self.valid_user.resume.delete(save=True)

	def test_website_field_exists(self):
		field = self.user._meta.get_field('website')
		self.assertTrue(isinstance(field, URLField))

	def test_github_profile_field_exists(self):
		field = self.user._meta.get_field('github_profile')
		self.assertTrue(isinstance(field, URLField))

	def test_linkedin_profile_field_exists(self):
		field = self.user._meta.get_field('linkedin_profile')
		self.assertTrue(isinstance(field, URLField))

import os
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.models import ImageField, FileField, URLField, TextField, CharField, BooleanField, ForeignKey
from django.core.files import File

# Create your tests here.
from portfolio_api.models import User, Project, Screenshot
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

class UserModelTest(TestCase):
	""" This class defines the test suite for the custom User model """
	@classmethod
	def setUpTestData(self):
		# set up data and variables available for all test methods
		# a user with all required fields set
		self.valid_user = User.objects.create(username='geek', password='password', first_name='Geek', last_name='User', email='geek@example.com')

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
		self.assertEquals(field.max_length, 300)

	def test_image_field_exists_and_saves_image_correctly(self):
		field = self.user._meta.get_field('image')
		self.assertTrue(isinstance(field, ImageField))
		img = File(open(os.path.join(CURRENT_DIR, 'test.jpg'), 'rb'))
		self.valid_user.image = img
		self.valid_user.save()
		
		# file will be saved in a subdirectory of media named after the user id
		self.assertIn("uploads/user_{0!s}/test.jpg".format(self.valid_user.id), self.valid_user.image.path)
		
		# close file and delete the uploaded file
		img.close
		self.valid_user.image.delete(save=True)

	def test_resume_field_exists_and_saves_file_correctly(self):
		field = self.user._meta.get_field('resume')
		self.assertTrue(isinstance(field, FileField))
		resume = File(open(os.path.join(CURRENT_DIR, 'test.doc'), 'rb'))
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

class ScreenshotModelTest(TestCase):
	""" This class defines the test suite for the Screenshot model """
	@classmethod
	def setUpTestData(self):
		# set up data and variables available for all test methods
		self.user = User.objects.create(username='genius', password='password', first_name='Genius', last_name='User', email='genius@example.com')
		self.project = Project.objects.create(user=self.user, name='XYZ Portfolios', short_description='XYZ portfolio site', role='FE: designed the front end')
		self.shot = Screenshot.objects.create(project=self.project, caption='User login page')
		
	def test_image_field_is_present_and_saves_correctly(self):
		field = self.user._meta.get_field('image')
		self.assertTrue(isinstance(field, ImageField))
		img = File(open(os.path.join(CURRENT_DIR, 'test.jpg'), 'rb'))
		self.shot.image = img
		self.shot.save()
		
		# file will be saved in a subdirectory of media named after the user id
		self.assertIn("uploads/user_{0!s}/test.jpg".format(self.user.id), self.shot.image.path)
		
		# close file and delete the uploaded file
		img.close
		self.shot.image.delete(save=True)

	def test_caption_field_is_present_as_char_field_with_right_limit(self):
		field = self.shot._meta.get_field('caption')
		self.assertTrue(isinstance(field, CharField))
		self.assertEquals(field.max_length, 50)

	def test_project_field_is_present_as_foreign_key_field(self): # Screenshot belongs to Project (Many to One)
		field = self.shot._meta.get_field('project')
		self.assertTrue(isinstance(field, ForeignKey))

class ProjectModelTest(TestCase):
	""" This class defines the test suite for the custom Project model """
	@classmethod
	def setUpTestData(self):
		# set up data and variables available for all test methods
		self.user = User.objects.create(username='nomad', password='password', first_name='Nomad', last_name='User', email='nomad@example.com')
		self.project = Project.objects.create(user=self.user, name='Portfolio Site', short_description='My portfolio site', role='Contributor, designed the db schema')
		
	def test_name_field_is_present_as_char_field_with_right_limit(self):
		field = self.project._meta.get_field('name')
		self.assertTrue(isinstance(field, CharField))
		self.assertEquals(field.max_length, 50)
		self.assertEquals(field.blank, False)

	def test_short_description_field_is_present_as_text_field_with_right_limit(self):
		field = self.project._meta.get_field('short_description')
		self.assertTrue(isinstance(field, CharField))
		self.assertEquals(field.max_length, 100)
		self.assertEquals(field.blank, False)

	def test_full_description_field_is_present_as_text_field_with_right_limit(self):
		field = self.project._meta.get_field('full_description')
		self.assertTrue(isinstance(field, TextField))
		self.assertEquals(field.max_length, 1000)
		self.assertEquals(field.blank, True)

	def test_description_field_is_present_as_text_field_with_right_limit(self):
		field = self.project._meta.get_field('tech_stack')
		self.assertTrue(isinstance(field, CharField))
		self.assertEquals(field.max_length, 200)
		self.assertEquals(field.blank, False)

	def test_role_field_is_present_as_text_field_with_right_limit(self):
		field = self.project._meta.get_field('role')
		self.assertTrue(isinstance(field, TextField))
		self.assertEquals(field.max_length, 300)
		self.assertEquals(field.blank, False)

	def test_private_field_is_present_as_boolean_field_with_right_deafault(self):
		field = self.project._meta.get_field('private')
		self.assertTrue(isinstance(field, BooleanField))
		self.assertEquals(field.default, False)

	def test_live_url_field_is_present_as_text_field_with_right_default(self):
		field = self.project._meta.get_field('live_url')
		self.assertTrue(isinstance(field, URLField))
		self.assertEquals(field.blank, True)

	def test_repo_url_field_is_present_as_text_field_with_right_default(self):
		field = self.project._meta.get_field('repo_url')
		self.assertTrue(isinstance(field, URLField))
		self.assertEquals(field.blank, True)

	def test_user_field_is_present_as_foreign_key_field(self): # Project belongs to User (Many to One)
		field = self.project._meta.get_field('user')
		self.assertTrue(isinstance(field, ForeignKey))

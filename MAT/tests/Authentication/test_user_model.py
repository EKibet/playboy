import pytest

from MAT.apps.authentication.models import User

class TestUserModel:
	@pytest.mark.django_db
	def test_create_new_user_succeeds(self):
		User.objects.create_user(
            username="Batman", email='test@mail.com')
		assert User.objects.filter(username='Batman').exists()

	@pytest.mark.django_db
	def test_create_super_user_succeeds(self):
		User.objects.create_superuser(
				username="Batman", email='test@mail.com', password='secret')
		assert User.objects.filter(username='Batman').exists()

	@pytest.mark.django_db
	def test_create_new_user_count_succeeds(self, new_user):
		new_user.save()
		assert User.objects.count() == 1

	def test_create_superuser_without_password_fails(self):
		with pytest.raises(TypeError) as excinfo:
			User.objects.create_superuser(
					username='Admin', email='test@mail.com', password=None)
			assert "Users must have a username." in str(excinfo.value)

	def test_create_user_without_username_fails(self):
		with pytest.raises(TypeError) as excinfo:
			User.objects.create_user(
				username=None, email='test@mail.com')
		assert "Users must have a username." in str(excinfo.value)

	def test_create_user_without_email_fails(self):
		with pytest.raises(TypeError) as excinfo:
			User.objects.create_user(
					username="Batman", email=None)
		assert "Users must have an email address." in str(excinfo.value)

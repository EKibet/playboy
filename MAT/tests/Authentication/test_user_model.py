import pytest

from MAT.apps.authentication.models import User


class TestUserModel:
	@pytest.mark.django_db
	def test_create_new_user_succeeds(self):
		User.objects.create_staff(
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
			User.objects.create_staff(
				username=None, email='test@mail.com')
		assert "Users must have a username." in str(excinfo.value)

	def test_create_user_without_email_fails(self):
		with pytest.raises(TypeError) as excinfo:
			User.objects.create_staff(
					username="Batman", email=None)
		assert "Users must have an email address." in str(excinfo.value)

	@pytest.mark.django_db
	def test_create_student_succeeds(self):
		User.objects.create_student(first_name="dave", last_name="kahara",
				username="Batman", email='test@mail.com', password='secret',cohort="mc23")
		assert User.objects.filter(username='Batman', is_student=True).exists()

	def test_create_student_without_username_fails(self):
		with pytest.raises(TypeError) as excinfo:
			User.objects.create_student(first_name="dave", last_name="kahara",
								email='test@mail.com', password='secret', username=None, cohort="mc23")
		assert "Students must have a username." in str(excinfo.value)

	def test_create_student_without_email_fails(self):
		with pytest.raises(TypeError) as excinfo:
			User.objects.create_student(first_name = "dave", last_name = "kahara",
                               username="Batman", password='secret', email=None, cohort="mc23")
		assert "Students must have an email address." in str(excinfo.value)

	def test_create_student_without_first_name_fails(self):
		with pytest.raises(TypeError) as excinfo:
			User.objects.create_student(first_name=None, last_name="kahara",
									username="Batman", password='secret', email="mail@me.com", cohort="mc23")
		assert "Students must have a first name." in str(excinfo.value)

	def test_create_student_without_last_name_fails(self):
		with pytest.raises(TypeError) as excinfo:
			User.objects.create_student(first_name="dave", last_name=None,
									username="Batman", password='secret', email='mail@me.com', cohort="mc23")
		assert "Students must have a last name." in str(excinfo.value)

	@pytest.mark.django_db
	def test_soft_delete_student_succeeds(self):
		user = User.objects.create_student(first_name="dave", last_name="kahara",
								username="Batman", email='test@mail.com', password='secret', cohort="mc23")
		assert User.objects.filter(username='Batman', is_student=True).exists()
		user.delete()
		assert user.deleted == True
		assert User.objects.filter(username='Batman', is_student=True).exists() == False

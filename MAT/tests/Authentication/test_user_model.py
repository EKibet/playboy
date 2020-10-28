import pytest
from django.db import IntegrityError

from MAT.apps.authentication.models import User, Student


class TestUserModel:
	@pytest.mark.django_db
	def test_create_new_user_succeeds(self):
		User.objects.create(
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

	@pytest.mark.django_db(transaction=True)
	def test_create_user_without_username_fails(self):
		with pytest.raises(IntegrityError) as excinfo:
			Student.objects.create(
				username=None, email='test@mail.com')
		assert "null value in column \"username\"" in str(excinfo.value)

	@pytest.mark.django_db
	def test_create_tm_without_email_fails(self):
		with pytest.raises(IntegrityError) as excinfo:
			Student.objects.create(
					username="Batman", email=None)
		assert "null value in column \"email\"" in str(excinfo.value)

	@pytest.mark.django_db
	def test_create_student_succeeds(self):
		Student.objects.create(first_name="dave", last_name="kahara",
				username="Batman", email='test@mail.com', password='secret')
		assert User.objects.filter(username='Batman', type="STUDENT").exists()

	@pytest.mark.django_db(transaction=True)
	def test_create_student_without_username_fails(self):
		with pytest.raises(IntegrityError) as excinfo:
			Student.objects.create(first_name="dave", last_name="kahara",
								email='test@mail.com', password='secret', username=None)
		assert "null value in column \"username\"" in str(excinfo.value)

	@pytest.mark.django_db(transaction=True)
	def test_create_student_without_email_fails(self):
		with pytest.raises(IntegrityError) as excinfo:
			Student.objects.create(first_name = "dave", last_name = "kahara",
                               username="Batman", password='secret', email=None,)
		assert "null value in column \"email\"" in str(excinfo.value)

	@pytest.mark.django_db(transaction=True)
	def test_create_student_without_first_name_fails(self):
		with pytest.raises(IntegrityError) as excinfo:
			Student.objects.create(first_name=None, last_name="kahara",
									username="Batman", password='secret', email="mail@me.com")
		assert "null value in column \"first_name\"" in str(excinfo.value)

	@pytest.mark.django_db(transaction=True)
	def test_create_student_without_last_name_fails(self):
		with pytest.raises(IntegrityError) as excinfo:
			Student.objects.create(first_name="dave", last_name=None,
									username="Batman", password='secret', email='mail@me.com')
		assert "null value in column \"last_name\"" in str(excinfo.value)

	@pytest.mark.django_db
	def test_soft_delete_student_succeeds(self):
		user = Student.objects.create(first_name="dave", last_name="kahara",
								username="Batman", email='test@mail.com', password='secret')
		assert Student.objects.filter(username='Batman').exists()
		user.delete()
		assert user.deleted == True
		assert user.is_active == False



import pytest
from MAT.apps.cohorts.models import Cohort
from MAT.apps.authentication.utility import student_cohort_assignment

class TestCohortAssignment:
    @pytest.mark.django_db
    def test_create_formated_cohort(self):
        student_cohort_assignment('    mc 0 1')
        assert Cohort.objects.filter(name='MC01').exists()

    @pytest.mark.django_db
    def test_get_existing_cohort(self):
        cohort =Cohort.objects.create(name='MC01')
        assert student_cohort_assignment('MC01') == cohort

    @pytest.mark.django_db
    def test_returns_none_if_field_is_null(self):
        name = ''
        student_cohort_assignment(name)
        assert len(Cohort.objects.all())==0

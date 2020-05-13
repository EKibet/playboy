from MAT.apps.cohorts.models import Cohort

def student_cohort_assignment(cohort_name):
    '''
        This is a utility that method assigns a cohort to a student at runtime:
            - checks if cohort exists else creates a cohort from the params
            - Takes the cohort name as an argument
    '''
    if cohort_name:
        cohort_name = ''.join(character for character in cohort_name.upper() if character.isalnum())
        if Cohort.objects.filter(name=cohort_name).exists():
            return Cohort.objects.only('id').get(name=cohort_name)
        Cohort.objects.create(name=cohort_name)
        return Cohort.objects.only('id').get(name=cohort_name)
    else:
        return None
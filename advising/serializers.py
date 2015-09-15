from advising.models import Student, Advisor, StudentAdvisorRole
from rest_framework import serializers


# Simplified representations of the Advisor and Student models. These are
# suitable for listing all advisors / students, and for nesting an advisor's
# students in the AdvisorFullSerializer class (and vise versa).

class AdvisorSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='advisor-detail',
                                               lookup_field='username')

    class Meta:
        model = Advisor
        fields = ('username', 'first_name', 'last_name', 'url')


class StudentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='student-detail',
                                               lookup_field='username')

    class Meta:
        model = Student
        fields = ('username', 'first_name', 'last_name', 'url')


# Serializations of the relationships between advisors and students.

class StudentAdvisorsSerializer(serializers.ModelSerializer):
    advisor = AdvisorSerializer(read_only=True)
    role = serializers.ReadOnlyField(source='role.description')

    class Meta:
        model = StudentAdvisorRole
        fields = ('role', 'advisor',)


class AdvisorStudentsSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    role = serializers.ReadOnlyField(source='role.description')

    class Meta:
        model = StudentAdvisorRole
        fields = ('role', 'student',)


# Full serializations of the Advisor and Student models, including nested
# lists of their relationships.

class StudentFullSerializer(StudentSerializer):
    advisors = StudentAdvisorsSerializer(source='studentadvisorrole_set',
                                         many=True)

    class Meta:
        model = Student
        fields = ('username', 'univ_id', 'first_name', 'last_name',
                  'advisors')


class AdvisorFullSerializer(AdvisorSerializer):
    students = AdvisorStudentsSerializer(source='studentadvisorrole_set',
                                         many=True)

    class Meta:
        model = Advisor
        fields = ('username', 'univ_id', 'first_name', 'last_name',
                  'students')

from advising.models import Student, Advisor, StudentAdvisorRole
from rest_framework import serializers


class AdvisorRoleSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source='advisor.first_name')
    last_name = serializers.ReadOnlyField(source='advisor.last_name')
    username = serializers.ReadOnlyField(source='advisor.username')
    univ_id = serializers.ReadOnlyField(source='advisor.univ_id')
    role = serializers.ReadOnlyField(source='role.description')

    class Meta:
        model = StudentAdvisorRole
        fields = ('username', 'univ_id', 'first_name', 'last_name', 'role',)


class StudentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='student-detail',
                                               lookup_field='username')

    class Meta:
        model = Student
        fields = ('username', 'first_name', 'last_name', 'url')


class StudentCompleteSerializer(StudentSerializer):
    advisors = AdvisorRoleSerializer(source='studentadvisorrole_set',
                                     many=True)

    class Meta:
        model = Student
        fields = ('username', 'univ_id', 'first_name', 'last_name',
                  'advisors')


class AdviseeRoleSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    role = serializers.ReadOnlyField(source='role.description')

    class Meta:
        model = StudentAdvisorRole
        fields = ('role', 'student',)


class AdvisorSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='advisor-detail',
                                               lookup_field='username')

    class Meta:
        model = Advisor
        fields = ('username', 'first_name', 'last_name', 'url')


class AdvisorCompleteSerializer(AdvisorSerializer):
    advisees = AdviseeRoleSerializer(source='studentadvisorrole_set',
                                     many=True)

    class Meta:
        model = Advisor
        fields = ('username', 'univ_id', 'first_name', 'last_name',
                  'advisees')

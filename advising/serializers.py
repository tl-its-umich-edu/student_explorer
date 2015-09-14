from advising.models import Student, Advisor, StudentAdvisorRole
from rest_framework import serializers


class AdvisorRoleSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source='advisor.first_name')
    last_name = serializers.ReadOnlyField(source='advisor.last_name')
    role = serializers.ReadOnlyField(source='role.description')

    class Meta:
        model = StudentAdvisorRole
        fields = ('first_name', 'last_name', 'role',)


class StudentSerializer(serializers.ModelSerializer):
    advisors = AdvisorRoleSerializer(source='studentadvisorrole_set',
                                     many=True)

    class Meta:
        model = Student
        fields = ('id', 'username', 'univ_id', 'first_name', 'last_name',
                  'advisors')
        depth = 1


class AdviseeRoleSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source='student.first_name')
    last_name = serializers.ReadOnlyField(source='student.last_name')
    username = serializers.ReadOnlyField(source='student.username')
    univ_id = serializers.ReadOnlyField(source='student.univ_id')
    role = serializers.ReadOnlyField(source='role.description')

    class Meta:
        model = StudentAdvisorRole
        fields = ('username', 'univ_id', 'first_name', 'last_name', 'role',)


class AdvisorSerializer(serializers.ModelSerializer):
    advisees = AdviseeRoleSerializer(source='studentadvisorrole_set',
                                     many=True)

    class Meta:
        model = Advisor
        fields = ('id', 'username', 'univ_id', 'first_name', 'last_name',
                  'advisees')

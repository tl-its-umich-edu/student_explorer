from advising.models import Student, Advisor
from rest_framework import serializers


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'username', 'univ_id', 'first_name', 'last_name')


class AdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor
        fields = ('id', 'username', 'univ_id', 'first_name', 'last_name')

from advising.models import (Student, Advisor, Cohort, StudentAdvisorRole,
                             StudentClassSiteStatus,
                             StudentClassSiteAssignment,
                             ClassSite)
from rest_framework import serializers


class AdvisorSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='advisor-detail',
                                               lookup_field='username')
    students_url = serializers.HyperlinkedIdentityField(
        view_name='advisor-students-list', lookup_field='username')

    class Meta:
        model = Advisor
        fields = ('username', 'univ_id', 'first_name', 'last_name', 'url',
                  'students_url')


class CohortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cohort
        fields = ('code', 'description', 'group')


class ClassSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSite
        fields = ('code', 'description')


class StudentClassSiteStatusSummarySerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='class_site.description')
    status = serializers.ReadOnlyField(source='status.description')

    class Meta:
        model = StudentClassSiteStatus
        fields = ('name', 'status')


class StudentSummarySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='student-detail',
                                               lookup_field='username')
    class_sites_url = serializers.HyperlinkedIdentityField(
        view_name='student-classsite-list', lookup_field='username')
    cohorts = serializers.StringRelatedField(many=True)
    statuses = serializers.StringRelatedField(many=True)
    advisors = serializers.StringRelatedField(many=True)
    status_weight = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ('url', 'username', 'univ_id', 'first_name', 'last_name',
                  'advisors', 'cohorts', 'statuses', 'status_weight',
                  'class_sites_url')

    def get_status_weight(self, obj):
        weight = 0
        for status in obj.statuses.all():
            if status.description == 'Green':
                weight += 0
            elif status.description == 'Yellow':
                weight += 2
            elif status.description == 'Red':
                weight += 4
        return weight


# Serializations of the relationships between advisors and students.

class StudentAdvisorsSerializer(serializers.ModelSerializer):
    advisor = AdvisorSerializer(read_only=True)
    role = serializers.ReadOnlyField(source='role.description')

    class Meta:
        model = StudentAdvisorRole
        fields = ('role', 'advisor',)


class StudentClassSitesSerializer(serializers.ModelSerializer):
    description = serializers.ReadOnlyField(source='class_site.description')
    code = serializers.ReadOnlyField(source='class_site.code')
    status = serializers.ReadOnlyField(source='status.description')

    class Meta:
        model = StudentClassSiteStatus
        fields = ('description', 'code', 'status')


class StudentClassSiteDetailSerializer(serializers.ModelSerializer):
    description = serializers.ReadOnlyField(source='class_site.description')
    code = serializers.ReadOnlyField(source='class_site.code')

    class Meta:
        model = ClassSite
        fields = ('description', 'code',)


class AdvisorStudentsSerializer(serializers.ModelSerializer):
    # student = StudentSerializer(read_only=True)
    advisor_role = serializers.ReadOnlyField(source='role.description')
    first_name = serializers.ReadOnlyField(source='student.first_name')
    last_name = serializers.ReadOnlyField(source='student.last_name')
    username = serializers.ReadOnlyField(source='student.username')
    univ_id = serializers.ReadOnlyField(source='student.univ_id')

    class Meta:
        model = StudentAdvisorRole
        # fields = ('role', 'student',)
        fields = ('advisor_role', 'first_name', 'last_name', 'username',
                  'univ_id',)


class StudentFullSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='student-detail',
                                               lookup_field='username')
    advisors = StudentAdvisorsSerializer(source='studentadvisorrole_set',
                                         many=True, read_only=True)
    cohorts = CohortSerializer(many=True, read_only=True)
    class_sites = StudentClassSitesSerializer(
        source='studentclasssitestatus_set', many=True, read_only=True)

    class Meta:
        model = Student
        fields = ('username', 'univ_id', 'first_name', 'last_name', 'advisors',
                  'cohorts', 'class_sites', 'url')


class StudentClassSiteAssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentClassSiteAssignment
        fields = ('points_earned', 'points_possible', 'included_in_grade',
                  'grader_comment', 'weight')

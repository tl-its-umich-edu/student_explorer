from advising.models import (Student, Advisor, Mentor, Cohort, Assignment,
                             StudentAdvisorRole, StudentCohortMentor,
                             StudentClassSiteStatus,
                             StudentClassSiteAssignment,
                             ClassSite)
from rest_framework import serializers
from rest_framework.reverse import reverse
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)


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


class AdvisorRoleSerializer(AdvisorSerializer):
    """
    Like AdvisorSerializer, but adds the advisor's roles for a specific student
    """
    roles = serializers.SerializerMethodField(read_only=True)

    def get_roles(self, advisor):
        """
        Get a list of advisor's role descriptions for a student.

        :param advisor: Advisor object
        :type advisor: Advisor
        :return: A tuple of descriptions of all the advisor's roles
        :rtype: tuple
        """
        studentUsername = self.context['username']
        return (StudentAdvisorRole.objects
                .filter(student__username=studentUsername, advisor=advisor)
                .values_list('role__description', flat=True).distinct())

    class Meta(AdvisorSerializer.Meta):
        fields = AdvisorSerializer.Meta.fields + ('roles',)


class MentorSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
            view_name='mentor-detail', lookup_field='username')
    students_url = serializers.HyperlinkedIdentityField(
            view_name='mentor-students-list', lookup_field='username')
    cohorts = CohortSerializer(many=True)

    class Meta:
        model = Mentor
        fields = ('username', 'univ_id', 'first_name', 'last_name', 'url',
                  'students_url', 'cohorts',)


class ClassSiteSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='class-site-detail',
                                               lookup_field='code')
    terms = serializers.StringRelatedField(many=True)
    source_system = serializers.StringRelatedField()
    students_url = serializers.HyperlinkedIdentityField(
        view_name='class-site-students-list', lookup_field='code')

    class Meta:
        model = ClassSite
        fields = ('url', 'code', 'description', 'terms', 'source_system',
                  'students_url')


class StudentClassSiteHyperlink(serializers.HyperlinkedIdentityField):
    def get_queryset(self):
        return (Student.objects
                .get(username=self.kwargs['username'])
                .studentclasssitestatus_set.all()
                )

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'code': obj.class_site.code,
            'username': obj.student.username
        }

        return reverse(view_name, kwargs=url_kwargs, request=request,
                       format=format)


class StudentClassSiteStatusSummarySerializer(serializers.ModelSerializer):
    code = serializers.ReadOnlyField(source='class_site.code')
    name = serializers.ReadOnlyField(source='class_site.description')
    url = StudentClassSiteHyperlink(
            read_only=True,
            view_name='student-classsite-detail'
    )
    status = serializers.ReadOnlyField(source='status.description')
    status_trend = serializers.SerializerMethodField()

    class Meta:
        model = StudentClassSiteStatus
        fields = ('code', 'name', 'url', 'status', 'status_trend')

    def get_status_trend(self, studentClassSiteStatus):
        try:
            currentStatusOrder = int(studentClassSiteStatus.status.order)
            previousStatusOrder = int(studentClassSiteStatus.class_site.weeklystudentclasssitestatus_set \
                .filter(student=studentClassSiteStatus.student).exclude(week_end_date=None) \
                .order_by('week_end_date').last().status.order)
        except (AttributeError, TypeError):
            return None

        statusOrderDifference = previousStatusOrder - currentStatusOrder
        statusOrderTrend = {
            1: 'up',
            0: 'steady',
            -1: 'down',
        }

        return statusOrderTrend.get(cmp(statusOrderDifference, 0))


class StudentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='student-detail',
                                               lookup_field='username')
    class_sites_url = serializers.HyperlinkedIdentityField(
        view_name='student-classsite-list', lookup_field='username')
    advisors_url = serializers.HyperlinkedIdentityField(
        view_name='student-advisors-list', lookup_field='username')
    mentors_url = serializers.HyperlinkedIdentityField(
        view_name='student-mentors-list', lookup_field='username')
    cohorts = serializers.StringRelatedField(many=True)
    mentors = serializers.StringRelatedField(many=True)
    status_weight = serializers.SerializerMethodField()
    email_address = serializers.SerializerMethodField()
    class_site_statuses = StudentClassSiteStatusSummarySerializer(many=True, source='studentclasssitestatus_set')

    class Meta:
        model = Student
        fields = ('url', 'username', 'univ_id',
                  'first_name', 'last_name',
                  'mentors', 'cohorts', 'class_site_statuses',
                  'status_weight',
                  'email_address',
                  'class_sites_url', 'advisors_url', 'mentors_url')

    def get_status_weight(self, student):
        """
        Using the set of class site statuses for a Student, reduce them to a
        single number representing their "weight". It's very important to
        initialize the reduction with zero.

        :param student: The Student object being serialized
        :type student: advising.models_dev.Student | advisingumich.models.Student
        :return: Weight of Student's class statuses
        :rtype: int
        """

        weights = {
            'red': 4,
            'yellow': 2,
            'green': 0
            }

        return reduce(
                lambda sum, aClassStatus: sum + weights.get(
                    aClassStatus.status.description.lower(), 0),
                student.studentclasssitestatus_set.all(),
                0
        )

    def get_email_address(self, student):

        return student.username + '@umich.edu'


# Serializations of the relationships between advisors and students.



class StudentMentorSerializer(serializers.ModelSerializer):
    mentor = MentorSerializer(read_only=True)
    cohort = serializers.ReadOnlyField(source='cohort.description')

    class Meta:
        model = StudentCohortMentor
        fields = ('cohort', 'mentor',)


class StudentClassSiteSerializer(serializers.ModelSerializer):
    # description = serializers.ReadOnlyField(source='class_site.description')
    # code = serializers.ReadOnlyField(source='class_site.code')
    status = serializers.ReadOnlyField(source='status.description')
    class_site = ClassSiteSerializer()
    student = StudentSerializer()
    current_class_score_average = serializers.SerializerMethodField()
    current_student_score_average = serializers.SerializerMethodField()

    url = StudentClassSiteHyperlink(
        read_only=True,
        view_name='student-classsite-detail')
    assignments_url = StudentClassSiteHyperlink(
        read_only=True,
        view_name='student-classsite-assignment-list')
    history_url = StudentClassSiteHyperlink(
        read_only=True,
        view_name='student-classsite-history-list')

    def get_current_class_score_average(self, obj):
        try:
            return obj.class_site.classsitescore_set.get(
                class_site=obj.class_site).current_score_average
        except ObjectDoesNotExist:
            return None

    def get_current_student_score_average(self, obj):
        try:
            return obj.class_site.studentclasssitescore_set.get(
                class_site=obj.class_site,
                student=obj.student
            ).current_score_average
        except ObjectDoesNotExist:
            return None

    class Meta:
        model = StudentClassSiteStatus
        fields = ('url', 'class_site', 'student', 'status',
                  'current_class_score_average',
                  'current_student_score_average',
                  'assignments_url', 'history_url')


class AdvisorStudentSerializer(serializers.ModelSerializer):
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


class AssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        fields = ('description', 'code')


class StudentClassSiteAssignmentSerializer(serializers.ModelSerializer):
    assignment = AssignmentSerializer(read_only=True)
    due_date = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = StudentClassSiteAssignment
        fields = ('assignment',
                  'points_earned', 'points_possible', 'percentage', 'weight',
                  'class_points_earned', 'class_points_possible',
                  'class_percentage', 'relative_to_average',
                  'included_in_grade', 'grader_comment', 'due_date')

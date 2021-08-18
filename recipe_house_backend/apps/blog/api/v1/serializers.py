from rest_framework import serializers

from recipe_house_backend.apps.blog.models import Tag, Blog


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model
    """

    class Meta(object):
        model = Tag
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    """
    Serializer for Blog model
    """

    class Meta(object):
        model = Blog
        fields = '__all__'

# employee_count = serializers.SerializerMethodField()
#     organization_name = serializers.SerializerMethodField()
#
#     class Meta(object):
#         model = OrganizationMission
#         fields = ('id', 'organization', 'mission', 'organization_name', 'employee_count')
#         read_only_fields = ('organization_name', 'employee_count',)
#
#     def get_employee_count(self, obj):
#         return Employee.objects.get_by_filter(organization=obj.organization).count()
#
#     def get_organization_name(self, obj):
#         return obj.organization.name

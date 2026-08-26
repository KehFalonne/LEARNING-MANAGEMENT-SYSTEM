from rest_framework import serializers

from .models import Student


class StudentDashboardSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()
    programme_name = serializers.CharField(
        source="programme.name",
        read_only=True,
    )
    programme_code = serializers.CharField(
        source="programme.code",
        read_only=True,
    )
    level_name = serializers.CharField(
        source="level.name",
        read_only=True,
    )

    class Meta:
        model = Student

        fields = (
            "student_id",
            "full_name",
            "programme_name",
            "programme_code",
            "level_name",
            "admission_year",
            "status",
        )

    def get_full_name(self, obj):
        return obj.user.get_full_name()
from rest_framework import serializers

from plan.models import Questionnaire, SectionOne, SectionTwo


class QuestionnaireSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    section_one = serializers.SerializerMethodField(read_only=True)
    section_two = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Questionnaire
        fields = [
            'user', 'uuid', 'status', 'section_one', 'section_two'
        ]

    def get_section_one(self, obj):
        try:
            section = obj.section_one
        except Exception:
            return {}
        return SectionOneSerializer(section).data

    def get_section_two(self, obj):
        try:
            section = obj.section_two
        except Exception:
            return {}
        return SectionTwoSerializer(section).data


class SectionOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionOne
        fields = [
            'questionnaire', 'business_type', 'bracket', 'industry'
        ]


class SectionTwoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionTwo
        fields = [
            'questionnaire', 'investment', 'investment_size'
        ]

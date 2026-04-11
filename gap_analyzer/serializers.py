from rest_framework import serializers

class JobDescriptionSerializer(serializers.Serializer):
    company_name = serializers.CharField()
    role = serializers.CharField()
    company_skills = serializers.ListField(child=serializers.CharField())
from rest_framework import serializers
from .models import Service,Category,Skill,Certificate





class SkillSerializer(serializers.ModelSerializer):
    percent_description = serializers.SerializerMethodField()

    class Meta:
        model = Skill
        fields = ['name', 'percent', 'percent_description']

    def get_percent_description(self, obj):
        percent = int(obj.percent[:-1]) * 0.01
        if percent <=0.2 :
            return "Poor"
        elif percent <= 0.4:
            return "Beginner"
        if percent <= 0.5:
            return "Normal"
        elif percent <= 0.7:
            return "Very Good"
        elif percent < 0.9:
            return "Great"
        else:
            return "Awesome"

    def validate_percent(self, value):
        if not value.endswith('%'):
            raise serializers.ValidationError('Percentage must end with a % symbol')
        try:
            percent = int(value[:-1])
            if not (0 <= percent <= 100):
                raise serializers.ValidationError('Percentage must be between 0 and 100')
        except ValueError:
            raise serializers.ValidationError('Invalid percentage value')
        return value

    def validate(self, data):
        user = self.context['request'].user
        percent = data.get('percent')
        self.validate_percent(percent)
        name=data.get('name')
        if Skill.objects.filter(user=user, name=name).exists():
            raise serializers.ValidationError('You have this Skill already')
        return data
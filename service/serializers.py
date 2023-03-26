from multiprocessing.sharedctypes import Value
from rest_framework import serializers
from .models import Service,Category,Skill,Certificate,SellService





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
        if value is not None:
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
        name = data.get('name')
        percent = data.get('percent')

        if self.instance and name == self.instance.name and percent == self.instance.percent:
            raise serializers.ValidationError('You did not make any changes')

        if name is not None and Skill.objects.filter(user=user, name=name).exists() and (not self.instance or name != self.instance.name):
            raise serializers.ValidationError('You have this Skill already')

        if name is None and percent == self.instance.percent or percent is None and name == self.instance.name:
            raise serializers.ValidationError('You did not make any changes')

        if 'name' not in data and 'percent' not in data:
            raise serializers.ValidationError('You did not make any changes')

        return data

       



class CertificateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Certificate
        fields = ['name', 'image']

    def validate(self, data):
        user = self.context['request'].user
        name = data.get('name')
        image = data.get('image')

        if self.instance and name == self.instance.name and image == self.instance.image:
            raise serializers.ValidationError('You did not make any changes')

        if name is not None and Skill.objects.filter(user=user, name=name).exists() and (not self.instance or name != self.instance.name):
            raise serializers.ValidationError('You have this Certificate already')

        if name is None and image == self.instance.image or image is None and name == self.instance.name:
            raise serializers.ValidationError('You did not make any changes')

        if 'name' not in data and 'image' not in data:
            raise serializers.ValidationError('You did not make any changes')

        return data


class ServiceSerializer(serializers.ModelSerializer):

    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())
    
    class Meta:
        model = Service
        fields = ['title','description','categories','price','delivery_time','revisions']

    def validate(self, data):
        title=data.get('title')
        if not title.isalnum():
            raise serializers.ValidationError('Title must not have any Symbol')
        return data



class SellServiceSerializer(serializers.ModelSerializer):

    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())
    
    class Meta:
        model = SellService
        fields = ['title','description','categories','price','delivery_time','revisions']

    def validate(self, data):
        title=data.get('title')
        if not title.isalnum():
            raise serializers.ValidationError('Title must not have any Symbol')
        return data
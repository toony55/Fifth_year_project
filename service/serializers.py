from multiprocessing.sharedctypes import Value
from rest_framework import serializers
from .models import Service,Category,Skill,Certificate,SellService,Request,SellRequest,Rating,Report





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
    buyer = serializers.StringRelatedField()
    class Meta:
        model = Service
        fields = ['id','title','description','categories','price','delivery_time','revisions','buyer','is_taken']



    def validate(self, data):
        title=data.get('title')
        if not title.isalnum():
            raise serializers.ValidationError('Title must not have any Symbol')
        return data



class SellServiceSerializer(serializers.ModelSerializer):

    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())
    
    class Meta:
        model = SellService
        fields = ['title','description','categories','price','delivery_time','revisions','seller']

    def validate(self, data):
        title=data.get('title')
        if not title.isalnum():
            raise serializers.ValidationError('Title must not have any Symbol')
        return data
    



class RequestSerializer(serializers.ModelSerializer):
    service_id = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), source='service')

    class Meta:
        model = Request
        fields = ['id', 'seller', 'buyer', 'service', 'status', 'created_at','service_id']
        read_only_fields = ['id', 'seller', 'created_at','buyer','service']

class SellRequestSerializer(serializers.ModelSerializer):
    service_id = serializers.PrimaryKeyRelatedField(queryset=SellService.objects.all(), source='service')

    class Meta:
        model = SellRequest
        fields = ['id', 'seller', 'buyer', 'service', 'status', 'created_at','service_id']
        read_only_fields = ['id', 'seller', 'created_at','buyer','service']




class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'rated_user', 'rating_user', 'value', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['rated_user', 'rating_user']

    
    def validate_value(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Value must be between 1 and 5.")
        return value
    
    def validate(self, data):
        value = data.get('value')
        comment = data.get('comment')

        if self.instance and value == self.instance.value and comment == self.instance.comment:
            raise serializers.ValidationError('You did not make any changes')

        if value is None and comment == self.instance.comment or comment is None and value == self.instance.value:
            raise serializers.ValidationError('You did not make any changes')

        if 'value' not in data and 'comment' not in data:
            raise serializers.ValidationError('You did not make any changes')
        
        return data
    

class ReportSerializer(serializers.ModelSerializer):
    reason_text = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = ['id','reason', 'other_reason','reporter','reported','created_at','other_reason','reason_text']
        read_only_fields = ['id','reporter', 'reported']

    def get_reason_text(self, obj):
        reason = obj.reason
        other_reason = obj.other_reason

        if other_reason:
            return f'"{other_reason}"'
        else:
            return dict(self.Meta.model.REPORT_REASON_CHOICES)[reason]
        
    def validate(self, data):
        reason = data.get('reason')
        other_reason = data.get('other_reason')

        if reason == 'Other' and not other_reason:
            raise serializers.ValidationError("If you select 'Other' as the reason, you must provide a description.")
        
        if other_reason:
            reason_text = f"{other_reason}"
        else:
            reason_text= dict(self.Meta.model.REPORT_REASON_CHOICES)[reason]

        return data



class CategorySerializer(serializers.ModelSerializer):
    num_services = serializers.SerializerMethodField()

    def get_num_services(self, obj):
        return Service.objects.filter(categories=obj).count()


    class Meta:
         model=Category
         fields=['image','description','name','num_services']
    

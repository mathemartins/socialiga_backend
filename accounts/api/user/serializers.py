from django.contrib.auth import get_user_model
from django.utils.datetime_safe import date
from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from accounts.models import Profile

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    image_uri = serializers.SerializerMethodField(read_only=True)
    uuid = serializers.SerializerMethodField()
    account_type = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    date_of_birth = serializers.SerializerMethodField(read_only=True)
    age = serializers.SerializerMethodField(read_only=True)
    slug = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'uuid',
            'gender',
            'phone',
            'date_of_birth',
            'age',
            'slug',
            'timestamp',
            'updated',
            'email',
            'image_uri',
            'account_type',
            'uri',
        ]

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse("api-user:detail", kwargs={"username": obj.username}, request=request)

    def get_image_uri(self, obj: User):
        instance = Profile.objects.get(user=obj)
        return instance.get_image

    def get_uuid(self, obj: User):
        instance = Profile.objects.get(user=obj)
        return instance.uuid

    def get_account_type(self, obj: User):
        instance = Profile.objects.get(user=obj)
        return instance.account_type

    def get_gender(self, obj: User):
        instance = Profile.objects.get(user=obj)
        return instance.gender

    def get_phone(self, obj: User):
        instance = Profile.objects.get(user=obj)
        return instance.phone

    def get_date_of_birth(self, obj: User):
        instance = Profile.objects.get(user=obj)
        return instance.date_of_birth

    def get_age(self, obj: User):
        instance = Profile.objects.get(user=obj)
        if instance.date_of_birth:
            today = date.today()
            return today.year - instance.date_of_birth.year - (
                    (today.month, today.day) < (instance.date_of_birth.month, instance.date_of_birth.day))
        return 0

    def get_slug(self, obj: User):
        instance = Profile.objects.get(user=obj)
        return instance.slug

    def get_timestamp(self, obj: User):
        instance = Profile.objects.get(user=obj)
        return instance.timestamp

    def get_updated(self, obj: User):
        instance = Profile.objects.get(user=obj)
        return instance.updated
from rest_framework import serializers
from .models import *


class FileListSterializer(serializers.Serializer):
    files = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False, use_url=False, max_length=1000000)
    )

    uploaded_by = serializers.EmailField()

    def create(self, validated_data):  # validated data is a dictionary
        uploaded_by = validated_data['uploaded_by']

        # folder = str(uploaded_by)
        # print(folder)
        files = validated_data.get('files')
        print(validated_data)  # pop removes the key from original dictionary
        file_objs = []
        for file in files:
            file_ob = File.objects.create(uploaded_by=uploaded_by, file=file)
            file_objs.append(file_ob)

        return validated_data

class UserSterializer(serializers.Serializer):
    uid = serializers.CharField()
    email = serializers.EmailField()
    premium = serializers.BooleanField(required=False)
    used_space = serializers.DecimalField(max_digits=10,decimal_places=3,required=False)
    def create(self, validated_data):
        return  User.objects.create(**validated_data)
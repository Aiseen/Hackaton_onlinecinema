from rest_framework import serializers

from apps.towatch.models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contact
        fields = '__all__'
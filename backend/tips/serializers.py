from rest_framework import serializers
from .models import Tip

class TipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tip
        fields = ['id','title','content','category','author','created_at','is_approved']

        read_only_fields = ['author','is_approved']
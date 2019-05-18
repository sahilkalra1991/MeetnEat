from rest_framework import serializers
from django.utils import timezone


class DateTimeTZField(serializers.DateTimeField):
    """
    DateTime field to return Date Time in Local time zone
    """
    def to_representation(self, value):
        value = timezone.localtime(value)
        return super(DateTimeTZField, self).to_representation(value)

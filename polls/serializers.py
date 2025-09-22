from rest_framework import serializers
from .models import Poll, Option, Vote


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text']


class PollSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ['id', 'title', 'description', 'created_at', 'expires_at', 'options']


class PollCreateSerializer(serializers.ModelSerializer):
    options = serializers.ListField(
        child=serializers.CharField(allow_blank=False, max_length=255),
        allow_empty=False,
        write_only=True,
    )

    class Meta:
        model = Poll
        fields = ['id', 'title', 'description', 'expires_at', 'options']

    def create(self, validated_data):
        option_texts = validated_data.pop('options')
        poll = Poll.objects.create(**validated_data)
        Option.objects.bulk_create([Option(poll=poll, text=text) for text in option_texts])
        return poll


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'poll', 'option', 'voter_id']
        extra_kwargs = {
            'poll': {'write_only': True},
        }

    def validate(self, attrs):
        poll = attrs['poll']
        option = attrs['option']
        if option.poll_id != poll.id:
            raise serializers.ValidationError('Option does not belong to the poll')
        if poll.expires_at is not None:
            from django.utils import timezone
            if timezone.now() > poll.expires_at:
                raise serializers.ValidationError('Poll has expired')
        return attrs


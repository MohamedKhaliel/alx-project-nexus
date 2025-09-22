from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Poll, Option, Vote
from .serializers import PollSerializer, VoteSerializer, PollCreateSerializer


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all().prefetch_related('options')
    serializer_class = PollSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['create']:
            return PollCreateSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=['post'])
    def vote(self, request, pk=None):
        serializer = VoteSerializer(data={
            'poll': pk,
            'option': request.data.get('option'),
            'voter_id': request.data.get('voter_id'),
        })
        serializer.is_valid(raise_exception=True)
        vote = serializer.save()
        return Response({'id': vote.id}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        poll = self.get_object()
        counts = (
            Vote.objects.filter(poll=poll)
            .values('option')
            .annotate(votes=Count('id'))
        )
        option_id_to_votes = {row['option']: row['votes'] for row in counts}
        results = [
            {
                'option_id': option.id,
                'text': option.text,
                'votes': option_id_to_votes.get(option.id, 0),
            }
            for option in poll.options.all()
        ]
        return Response({'poll_id': poll.id, 'title': poll.title, 'results': results})

# Create your views here.

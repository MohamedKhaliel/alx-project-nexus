from django.db import models


class Poll(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title


class Option(models.Model):
    poll = models.ForeignKey(Poll, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    class Meta:
        unique_together = ('poll', 'text')
        indexes = [
            models.Index(fields=['poll']),
        ]

    def __str__(self) -> str:
        return f"{self.poll_id}: {self.text}"


class Vote(models.Model):
    poll = models.ForeignKey(Poll, related_name='votes', on_delete=models.CASCADE)
    option = models.ForeignKey(Option, related_name='votes', on_delete=models.CASCADE)
    voter_id = models.CharField(max_length=255)
    cast_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('poll', 'voter_id')
        indexes = [
            models.Index(fields=['poll']),
            models.Index(fields=['option']),
        ]

    def __str__(self) -> str:
        return f"vote p{self.poll_id} o{self.option_id} by {self.voter_id}"

# Create your models here.

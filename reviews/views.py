from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from account.permissions import IsUserOrAdmin
from .models import Review
from .serializers import ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    METHODS = ['PATCH', 'PUT', 'DELETE', 'POST']

    @action(detail=True, methods=['GET'])
    def get_song_rating(self, request):
        song_rating = Review.objects.filter(song=request.data['song'])
        serializer = ReviewSerializer(song_rating, many=True)
        return Response(serializer.data)
    def get_permissions(self):
        if self.request.method in self.METHODS:
            return [IsUserOrAdmin()]
        return [permissions.AllowAny()]
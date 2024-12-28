from rest_framework.response import Response

from reviews.serializers import ReviewSerializer
from .models import Song
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

from account.permissions import IsUserOrAdmin
from .serializers import SongSerializer


class SongCreateView(generics.CreateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = SongSerializer


class SongListView(generics.ListAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

class SongDetailView(generics.RetrieveAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = (IsAdminUser, )


class SongUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class SongDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Song.objects.all()


class ReviewAddView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsUserOrAdmin]

    def perform_create(self, serializer):
        song_id = self.kwargs.get('song_id')
        song = generics.get_object_or_404(Song, id=song_id)

        existing_review = song.reviews.filter(reviewer=self.request.user).first()
        if existing_review:
            # Если отзыв существует, удаляем его
            existing_review.delete()

        # Создаем новый отзыв
        serializer.save(
            reviewer=self.request.user,  # Передаем текущего пользователя
            music=song  # Привязываем песню
        )

    def get_serializer_context(self):
        """
        Добавляем текущего пользователя и объект песни в контекст сериализатора.
        """
        context = super().get_serializer_context()
        song_id = self.kwargs.get('song_id')
        context['song'] = generics.get_object_or_404(Song, id=song_id)
        return context

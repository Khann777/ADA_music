from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework import generics

from .models import Song
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


from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from account.permissions import IsUserOrAdmin
from .models import Song
from .serializers import SongSerializer
from reviews.serializers import ReviewSerializer


class ReviewAddView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsUserOrAdmin]

    def perform_create(self, serializer):
        """
        Создаем новый отзыв. Уникальность отзыва контролируется с помощью unique_together в модели.
        """
        song_id = self.kwargs.get('song_id')
        song = get_object_or_404(Song, id=song_id)

        try:
            # Сохраняем новый отзыв
            serializer.save(
                reviewer=self.request.user,
                music=song
            )
        except ValidationError:
            # В случае нарушения уникальности отзыва для песни и пользователя
            raise ValidationError('Вы уже оставили отзыв для этой песни.')

    def create(self, request, *args, **kwargs):
        """
        Переопределяем метод create, чтобы добавить детализированный ответ.
        """
        response = super().create(request, *args, **kwargs)
        return Response({'detail': 'Отзыв добавлен'}, status=201)


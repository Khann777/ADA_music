from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    ADMIN_ACTIONS = ['create', 'update', 'destroy', 'approve', 'reject']

    def get_permissions(self):
        """
        Устанавливаем права доступа для различных методов.
        """
        if self.action in self.ADMIN_ACTIONS:
            return [IsAdminUser()] #? Администраторы могут изменять статус
        return [permissions.IsAuthenticated()]  #? Для других действий — обычная аутентификация

    def perform_create(self, serializer):
        """
        При создании заказа устанавливаем текущего пользователя как владельца.
        """
        serializer.save(customer=self.request.user)

    def get_queryset(self):
        """
        Если пользователь — администратор, он видит все заказы.
        Если пользователь — обычный, он видит только свои заказы.
        """
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(customer=user)


    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        order = self.get_object()
        order.status = 'approved'
        order.save()
        return Response({'detail': 'Order approved successfully.'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        order = self.get_object()
        order.status = 'rejected'
        order.save()
        return Response({'detail': 'Order rejected successfully.'})

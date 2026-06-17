from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from access_control.services import has_access


ORDERS = [
    {
        "id": 1,
        "title": "Order 1",
        "description": "First mock order",
        "owner_id": 2,
    },
    {
        "id": 2,
        "title": "Order 2",
        "description": "Second mock order",
        "owner_id": 3,
    },
    {
        "id": 3,
        "title": "Order 3",
        "description": "Third mock order",
        "owner_id": 1,
    },
]


def get_order(order_id):
    for order in ORDERS:
        if order["id"] == order_id:
            return order

    raise NotFound("Order not found")


class OrderListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        available_orders = []

        for order in ORDERS:
            if has_access(
                user=request.user,
                element_code="orders",
                action="read",
                owner_id=order["owner_id"],
            ):
                available_orders.append(order)

        return Response(available_orders)

    def post(self, request):
        if not has_access(
            user=request.user,
            element_code="orders",
            action="create",
        ):
            raise PermissionDenied("You do not have permission to create orders")

        new_order = {
            "id": len(ORDERS) + 1,
            "title": request.data.get("title", "Untitled order"),
            "description": request.data.get("description", ""),
            "owner_id": request.user.id,
        }

        ORDERS.append(new_order)

        return Response(
            new_order,
            status=status.HTTP_201_CREATED,
        )


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = get_order(pk)

        if not has_access(
            user=request.user,
            element_code="orders",
            action="read",
            owner_id=order["owner_id"],
        ):
            raise PermissionDenied("You do not have permission to read this order")

        return Response(order)

    def patch(self, request, pk):
        order = get_order(pk)

        if not has_access(
            user=request.user,
            element_code="orders",
            action="update",
            owner_id=order["owner_id"],
        ):
            raise PermissionDenied("You do not have permission to update this order")

        order["title"] = request.data.get("title", order["title"])
        order["description"] = request.data.get(
            "description",
            order["description"],
        )

        return Response(order)

    def delete(self, request, pk):
        order = get_order(pk)

        if not has_access(
            user=request.user,
            element_code="orders",
            action="delete",
            owner_id=order["owner_id"],
        ):
            raise PermissionDenied("You do not have permission to delete this order")

        ORDERS.remove(order)

        return Response(status=status.HTTP_204_NO_CONTENT)
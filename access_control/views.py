from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from access_control.models import AccessRoleRule, BusinessElement, Role, UserRole
from access_control.permissions import AccessRulesPermission
from access_control.serializers import (
    AccessRoleRuleSerializer,
    BusinessElementSerializer,
    RoleSerializer,
    UserRoleSerializer,
)


class RoleListCreateView(APIView):
    permission_classes = [IsAuthenticated, AccessRulesPermission]

    def get(self, request):
        roles = Role.objects.all().order_by("id")
        serializer = RoleSerializer(roles, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        role = serializer.save()

        return Response(
            RoleSerializer(role).data,
            status=status.HTTP_201_CREATED,
        )


class RoleDetailView(APIView):
    permission_classes = [IsAuthenticated, AccessRulesPermission]

    def get_object(self, pk):
        return Role.objects.get(pk=pk)

    def get(self, request, pk):
        role = self.get_object(pk)
        serializer = RoleSerializer(role)

        return Response(serializer.data)

    def patch(self, request, pk):
        role = self.get_object(pk)
        serializer = RoleSerializer(role, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        role = serializer.save()

        return Response(RoleSerializer(role).data)

    def delete(self, request, pk):
        role = self.get_object(pk)
        role.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class BusinessElementListCreateView(APIView):
    permission_classes = [IsAuthenticated, AccessRulesPermission]

    def get(self, request):
        elements = BusinessElement.objects.all().order_by("id")
        serializer = BusinessElementSerializer(elements, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = BusinessElementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        element = serializer.save()

        return Response(
            BusinessElementSerializer(element).data,
            status=status.HTTP_201_CREATED,
        )


class BusinessElementDetailView(APIView):
    permission_classes = [IsAuthenticated, AccessRulesPermission]

    def get_object(self, pk):
        return BusinessElement.objects.get(pk=pk)

    def get(self, request, pk):
        element = self.get_object(pk)
        serializer = BusinessElementSerializer(element)

        return Response(serializer.data)

    def patch(self, request, pk):
        element = self.get_object(pk)
        serializer = BusinessElementSerializer(
            element,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        element = serializer.save()

        return Response(BusinessElementSerializer(element).data)

    def delete(self, request, pk):
        element = self.get_object(pk)
        element.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class AccessRoleRuleListCreateView(APIView):
    permission_classes = [IsAuthenticated, AccessRulesPermission]

    def get(self, request):
        rules = AccessRoleRule.objects.select_related(
            "role",
            "element",
        ).all().order_by("id")

        serializer = AccessRoleRuleSerializer(rules, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = AccessRoleRuleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rule = serializer.save()

        return Response(
            AccessRoleRuleSerializer(rule).data,
            status=status.HTTP_201_CREATED,
        )


class AccessRoleRuleDetailView(APIView):
    permission_classes = [IsAuthenticated, AccessRulesPermission]

    def get_object(self, pk):
        return AccessRoleRule.objects.select_related(
            "role",
            "element",
        ).get(pk=pk)

    def get(self, request, pk):
        rule = self.get_object(pk)
        serializer = AccessRoleRuleSerializer(rule)

        return Response(serializer.data)

    def patch(self, request, pk):
        rule = self.get_object(pk)
        serializer = AccessRoleRuleSerializer(
            rule,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        rule = serializer.save()

        return Response(AccessRoleRuleSerializer(rule).data)

    def delete(self, request, pk):
        rule = self.get_object(pk)
        rule.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRoleListCreateView(APIView):
    permission_classes = [IsAuthenticated, AccessRulesPermission]

    def get(self, request):
        user_roles = UserRole.objects.select_related(
            "user",
            "role",
        ).all().order_by("id")

        serializer = UserRoleSerializer(user_roles, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = UserRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_role = serializer.save()

        return Response(
            UserRoleSerializer(user_role).data,
            status=status.HTTP_201_CREATED,
        )


class UserRoleDetailView(APIView):
    permission_classes = [IsAuthenticated, AccessRulesPermission]

    def get_object(self, pk):
        return UserRole.objects.select_related("user", "role").get(pk=pk)

    def get(self, request, pk):
        user_role = self.get_object(pk)
        serializer = UserRoleSerializer(user_role)

        return Response(serializer.data)

    def patch(self, request, pk):
        user_role = self.get_object(pk)
        serializer = UserRoleSerializer(
            user_role,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        user_role = serializer.save()

        return Response(UserRoleSerializer(user_role).data)

    def delete(self, request, pk):
        user_role = self.get_object(pk)
        user_role.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
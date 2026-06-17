from django.urls import path

from access_control.views import (
    AccessRoleRuleDetailView,
    AccessRoleRuleListCreateView,
    BusinessElementDetailView,
    BusinessElementListCreateView,
    RoleDetailView,
    RoleListCreateView,
    UserRoleDetailView,
    UserRoleListCreateView,
)


urlpatterns = [
    path("roles/", RoleListCreateView.as_view(), name="roles"),
    path("roles/<int:pk>/", RoleDetailView.as_view(), name="role-detail"),

    path(
        "elements/",
        BusinessElementListCreateView.as_view(),
        name="business-elements",
    ),
    path(
        "elements/<int:pk>/",
        BusinessElementDetailView.as_view(),
        name="business-element-detail",
    ),

    path("rules/", AccessRoleRuleListCreateView.as_view(), name="rules"),
    path(
        "rules/<int:pk>/",
        AccessRoleRuleDetailView.as_view(),
        name="rule-detail",
    ),

    path("user-roles/", UserRoleListCreateView.as_view(), name="user-roles"),
    path(
        "user-roles/<int:pk>/",
        UserRoleDetailView.as_view(),
        name="user-role-detail",
    ),
]
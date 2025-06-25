# meu_saas_projeto/backend/core/urls.py

from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # URLs de autenticação e páginas principais
    path("", views.homepage, name="homepage"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="homepage"), name="logout"),
    path("register/", views.register, name="register"),
    # URLs para Produtos
    path("products/", views.product_list, name="products_list"),
    path("products/new/", views.product_create, name="product_create"),
    path("products/<int:pk>/edit/", views.product_update, name="product_update"),
    path("products/<int:pk>/delete/", views.product_delete, name="product_delete"),
    # URLs para Clientes
    path("clients/", views.client_list, name="client_list"),
    path("clients/new/", views.client_create, name="client_create"),
    path("clients/<int:pk>/edit/", views.client_update, name="client_update"),
    path("clients/<int:pk>/delete/", views.client_delete, name="client_delete"),
    # URLs para Resgates
    path(
        "resgates/",
        include(
            [
                path("", views.resgate_list, name="resgate_list"),
                path(
                    "importar/", views.resgate_upload_parse, name="resgate_upload_parse"
                ),
                path("<int:pk>/", views.resgate_detail, name="resgate_detail"),
                path("<int:pk>/excluir/", views.resgate_delete, name="resgate_delete"),
                # ADICIONE ESTA LINHA AQUI
                path(
                    "<int:pk>/update_status/",
                    views.update_resgate_status,
                    name="update_resgate_status",
                ),
                path(
                    "excluir-todos/",
                    views.resgate_delete_all,
                    name="resgate_delete_all",
                ),
                path(
                    "exportar-csv/", views.resgate_export_csv, name="resgate_export_csv"
                ),
                path(
                    "validar-rastreamento/",
                    views.resgate_validate_tracking,
                    name="resgate_validate_tracking",
                ),
            ]
        ),
    ),
    # URLs para Relatórios Gerados
    path(
        "reports/",
        include(
            [
                path("", views.report_list, name="report_list"),
                path(
                    "delete-selected/",
                    views.report_delete_selected,
                    name="report_delete_selected",
                ),
                path("delete-all/", views.report_delete_all, name="report_delete_all"),
                path(
                    "<int:pk>/delete/",
                    views.report_delete_single,
                    name="report_delete_single",
                ),
            ]
        ),
    ),
]

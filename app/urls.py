from django.urls import path

from app import views

app_name = "app"
urlpatterns = [
    path("weeks/", views.WeekListView.as_view(), name="week_list"),
    path("week/<int:pk>/", views.WeekDetailView.as_view(), name="week_detail"),
    path("training/<int:pk>/", views.TrainingDetailView.as_view(), name="week_detail"),
]

from rest_framework import generics
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response

from app import models, serializers


class DetailRelatedObjectsListMixin:
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        queryset = getattr(getattr(instance, self.related_objects_name, None), "all", [])()

        related_serializer = self.related_objects_serializer(queryset, many=True, context={"request": request})
        data[self.related_objects_name] = related_serializer.data
        return Response(data)


class DetailRelatedObjectsListAPIView(DetailRelatedObjectsListMixin,
                                      generics.GenericAPIView):
    """
    Concrete view for retrieving a model instance with related objects.
    """
    related_objects_name = None
    related_objects_serializer = None
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class WeekListView(generics.ListAPIView):
    queryset = models.Week.objects.all()
    serializer_class = serializers.WeekSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class WeekDetailView(DetailRelatedObjectsListAPIView):
    queryset = models.Week.objects.all()
    serializer_class = serializers.WeekSerializer
    related_objects_name = "trainings"
    related_objects_serializer = serializers.TrainingSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class TrainingDetailView(DetailRelatedObjectsListAPIView):
    queryset = models.Training.objects.all()
    serializer_class = serializers.TrainingSerializer
    related_objects_name = "exercises"
    related_objects_serializer = serializers.ExerciseSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

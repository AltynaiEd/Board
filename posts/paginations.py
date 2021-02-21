from rest_framework.pagination import LimitOffsetPagination


class Paginatin(LimitOffsetPagination):
    default_limit = 2
    max_limit = 3
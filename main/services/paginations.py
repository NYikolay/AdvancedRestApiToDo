from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PaginationTasks(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 25

    def get_paginated_response(self, data):
        return Response(data, headers={'count': self.page.paginator.count})


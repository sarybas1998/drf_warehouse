from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from urllib.parse import urlencode


class ListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })

    def get_next_link(self):
        if not self.page.has_next():
            return None
        url = self.request.build_absolute_uri()
        return self.replace_query_param(url, self.page_query_param, self.page.next_page_number())

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        url = self.request.build_absolute_uri()
        return self.replace_query_param(url, self.page_query_param, self.page.previous_page_number())

    def replace_query_param(self, url, key, val):
        querystring = self.request.query_params.copy()
        querystring[key] = val
        # Ensure 'q' is always the first parameter
        params = [(k, querystring[k]) for k in querystring.keys()]
        querystring = urlencode(params)
        return '{}?{}'.format(self.request.build_absolute_uri(self.request.path), querystring)

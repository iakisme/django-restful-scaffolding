from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    '''
        doing this class only to make page_size work...
    '''
    page_size_query_param = 'page_size'


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    def get_paginated_response(self, data):
        next_link_str = self.get_next_link()
        previous_link_str = self.get_previous_link()
        if next_link_str!=None and next_link_str.find("http://127.0.0.1:8000") == 0:
            next_link_str = next_link_str[21:]
        if previous_link_str != None and previous_link_str.find("http://127.0.0.1:8000") == 0:
            previous_link_str = previous_link_str[21:]
        return Response({
            'next': next_link_str,
            'previous': previous_link_str,
            'count': self.page.paginator.count,
            'results': data
        })

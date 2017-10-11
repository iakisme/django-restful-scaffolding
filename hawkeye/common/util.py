from rest_framework.response import Response
from rest_framework import status

def view_try_except(func,*args,**kw):
    def exec_func(*args,**kw):
        try:
            return func(*args,**kw)
        except Exception as e:
            error = e.args
            print( error )
            return Response({'error_message': error},status=status.HTTP_400_BAD_REQUEST)
    return exec_func
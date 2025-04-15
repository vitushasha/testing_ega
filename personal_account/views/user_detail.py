from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from personal_account.models.serializers import UserSerializer, DocumentsSerializer


class UserDetailApiView(APIView):
    def get(self, request, format=None):
        serializer_user = UserSerializer(request.user)
        docs = request.user.documents.all()
        params = request.query_params.get('doc_ids')
        if params:
            docs = [doc.data['id'] in params.strip(' []').split(',') for doc in docs]
        serializer_doc = DocumentsSerializer(docs, many=True)
        data = {'user_data': serializer_user.data, 'docs': serializer_doc.data}
        return Response(data, status=status.HTTP_200_OK)

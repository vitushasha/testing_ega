from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from personal_account.models.serializers import UserSerializer, DocumentsSerializer
from personal_account.utils.get_params import get_param


class UserDetailApiView(APIView):

    @get_param('doc_ids', list)
    def get(self, request, format=None):
        serializer_user = UserSerializer(request.user)
        docs = request.user.documents.all()
        if request.data.get('doc_ids'):
            param = request.data.get('doc_ids')
            docs = [doc.data['id'] in param for doc in docs]
        serializer_doc = DocumentsSerializer(docs, many=True)
        data = {'user_data': serializer_user.data, 'docs': serializer_doc.data}
        return Response(data, status=status.HTTP_200_OK)


from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from all.serializers.ProjectSerializer import ProjectSerializer
import gns3fy


class GetExistsTemplateWithid(GenericAPIView):
    """
    methode: get
    get one template details by id
    """
    serializer_class=()
    parser_classes = (FormParser, MultiPartParser)
    def get(self, request ,template_id):
        try:
            gns3_server = gns3fy.Gns3Connector("http://localhost:3080")
            template=gns3_server.get_template(template_id=id)
            return Response(data=template,status=status.HTTP_200_OK)
        except:
            return Response(data={"notice":"check the gns3 server"},status=status.HTTP_400_BAD_REQUEST)
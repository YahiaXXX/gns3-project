from pickle import NONE
import telnetlib
from time import sleep
from tkinter.font import names
from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from all.serializers.ProjectSerializer import AddVlanSerializer
import gns3fy
class deletenode(GenericAPIView):
    serializer_class=()
    #parser_classes = (FormParser, MultiPartParser)
    def delete(self, request ,project_id,node_id):
        #try: 
            gns3_server = gns3fy.Gns3Connector("http://localhost:3080")
            node=gns3fy.Node(connector=gns3_server,node_id=node_id,project_id=project_id)
            node.delete()
            return Response(status=status.HTTP_200_OK)
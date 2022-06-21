from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from all.serializers.ProjectSerializer import ProjectSerializer
import gns3fy

class openprojectview(GenericAPIView):
    """
    methode: get
    get all the projects exists en the server
    methode: post 
    create a new blank project
    """
    def post(self, request , project_id):
        try:
            gns3_server = gns3fy.Gns3Connector("http://localhost:3080")
            projet=gns3fy.Project(project_id=project_id,connector=gns3_server)
            projet.open()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(data={"notice":"check the gns3 server"},status=status.HTTP_400_BAD_REQUEST)
class closeprojetview(GenericAPIView):
    """
    methode: get
    get all the projects exists en the server
    methode: post 
    create a new blank project
    """
    def post(self, request , project_id):
        try:
            gns3_server = gns3fy.Gns3Connector("http://localhost:3080")
            projet=gns3fy.Project(project_id=project_id,connector=gns3_server)
            projet.close()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(data={"notice":"check the gns3 server"},status=status.HTTP_400_BAD_REQUEST)
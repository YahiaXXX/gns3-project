
from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from all.serializers.ProjectSerializer import ProjectSerializer
import gns3fy

class ProjectsViews(GenericAPIView):
    """
    methode: get
    get all the projects exists en the server

    methode: post 
    create a new blank project
    """
    serializer_class=ProjectSerializer
    # parser_classes = (FormParser, MultiPartParser)
    def get(self, request):
        try:
            gns3_server = gns3fy.Gns3Connector("http://localhost:3080")
            projects=gns3_server.get_projects()
            return Response(data=projects,status=status.HTTP_200_OK)
        except:
            return Response(data={"notice":"check the gns3 server"},status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        try:
            serializer=self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                gns3_server = gns3fy.Gns3Connector("http://localhost:3080")
                created_project=gns3_server.create_project(name=serializer.validated_data['name'])
                return Response(data=created_project,status=status.HTTP_201_CREATED)
        except:
            return Response(data={"notice":"check the gns3 server"},status=status.HTTP_400_BAD_REQUEST)

class GetProjectWithIdViews(GenericAPIView):
    """
    methode: get
    get informations about the project with specific id (one project)

    methode: delete
    delete a  project with specific id 
    """
    serializer_class=ProjectSerializer
    parser_classes = (FormParser, MultiPartParser)
    def get(self, request , project_id):
        try:
            gns3_server = gns3fy.Gns3Connector("http://localhost:3080")
            project=gns3_server.get_project(project_id=project_id)
            return Response(data=project,status=status.HTTP_200_OK)
        except:
            return Response(data={"notice":"check the gns3 server"},status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request , project_id):
        try:
            gns3_server = gns3fy.Gns3Connector("http://localhost:3080")
            project=gns3_server.delete_project(project_id=project_id)
            return Response(data=project,status=status.HTTP_200_OK)
        except:
            return Response(data={"notice":"check the gns3 server"},status=status.HTTP_400_BAD_REQUEST)

from http.client import ImproperConnectionState
from lib2to3.pytree import Node
from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from all.serializers.ProjectSerializer import ProjectSerializer
import gns3fy
from all.serializers.ProjectSerializer import Nodeserializer

class ProjectNodesView(GenericAPIView):
    """
    methode: get
    get all the nodes (topology)  of a project with id of the project
    """
    serializer_class=Nodeserializer
    #parser_classes = (FormParser, MultiPartParser)
    def get(self, request ,project_id):
        try:
            gns3_server = gns3fy.Gns3Connector("http://localhost:3080")
            templates=gns3_server.get_nodes(project_id=project_id)
            dict1={
                    "command_line": "",
                    "compute_id": "local",
                    "console_auto_start": "false",
                    "console_host": "localhost",
                    "custom_adapters": [],
                    "first_port_name": "null",
                    "height": 32,
                    "label": {
                    "rotation": 0,
                    "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
                    "text": "Switch2",
                    "x": -3,
                    "y": -25
                    },
                    "node_directory": "null",
                    "port_name_format": "Ethernet{0}",
                    "port_segment_size": 0,
                    "properties": {},
                    "width": 72,
                    "x": -864,
                    "y": 64,
                    "z": 1
                }
            
            for t in templates:
                a=gns3_server.get_template(template_id=t["template_id"])
                print(a["category"])
                t["category"]=a["category"]
                for x in dict1.keys():
                    t.pop(x,None)

            return Response(data=templates,status=status.HTTP_200_OK)
        except:
            return Response(data={"notice":"check the gns3 server"},status=status.HTTP_400_BAD_REQUEST)
    def post(self, request ,project_id):
        try:
            serializer=Nodeserializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            gns3_server = gns3fy.Gns3Connector("http://localhost:3080")
            project=gns3fy.Project(project_id=project_id,connector=gns3_server)
            project.open()
            node=gns3fy.Node(project_id=project_id,connector=gns3_server,template=serializer.validated_data['template'])
            node.create()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(data={"notice":"check the gns3 server"},status=status.HTTP_400_BAD_REQUEST)

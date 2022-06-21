
from http.client import ImproperConnectionState
from lib2to3.pytree import Node
from os import link
from re import L, S
from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from all.serializers.ProjectSerializer import ProjectSerializer
import gns3fy
from all.serializers.ProjectSerializer import Nodeserializer ,linkserializer
from tabulate import tabulate

class ProjectLinksView(GenericAPIView):
    """
methode: get
get all the links (topology)  of a project with id of the project
    """
    serializer_class=linkserializer
    parser_classes = (FormParser, MultiPartParser)
    def get(self, request ,project_id):
        #try:
            gns3_server = gns3fy.Gns3Connector("http://localhost:3080")
            links=gns3_server.get_links(project_id=project_id)
            links_summary = gns3fy.Project(project_id=project_id,connector=gns3_server).links_summary(is_print=False)
            list_of_links=[]
            for link in links:
                for i in link["nodes"]:
                    if i["node_id"]=="c115f874-3948-4e20-9980-f9d6c06e3adc":
                        list_of_links.append(i)
                        
            print (list_of_links)
            #print(link)
            print(
                links_summary
                )
            """
            for l in links :
                l.pop("capture_compute_id")
                l.pop("capture_file_name")
                l.pop("capture_file_path")
                l.pop("capturing")
                l.pop("filters")
                l.pop("link_style")
                for b in l["nodes"]:
                    b.pop("label")
            """
            return Response(data=links_summary,status=status.HTTP_200_OK)
        #except:
            return Response(data={"notice":"check the gns3 server"},status=status.HTTP_400_BAD_REQUEST)
    def post(self, request ,project_id):
        try:
            serializer=linkserializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            gns3_server = gns3fy.Gns3Connector("http://localhost:3080")
            nodes = [
                dict(node_id=serializer.validated_data["node_id_1"], adapter_number=serializer.validated_data["node_id_1_adapter_number"]
                , port_number=serializer.validated_data["node_id_1_port_number"]),
                                dict(node_id=serializer.validated_data["node_id_2"], adapter_number=serializer.validated_data["node_id_2_adapter_number"]
                , port_number=serializer.validated_data["node_id_2_port_number"]),
                    ]

            project=gns3fy.Project(project_id=project_id,connector=gns3_server )
            project.open()

            node=gns3fy.Link(project_id=project_id,connector=gns3_server,nodes=nodes)
            node.create()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(data={"notice":"check the gns3 server"},status=status.HTTP_400_BAD_REQUEST)
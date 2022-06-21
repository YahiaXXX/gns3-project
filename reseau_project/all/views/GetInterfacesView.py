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





class GetInterfacesView(GenericAPIView):
    serializer_class=AddVlanSerializer
    parser_classes = (FormParser, MultiPartParser)
    def get(self, request ,project_id,node_id):
        gns3_server = gns3fy.Gns3Connector("http://localhost:3080")
        links=gns3_server.get_links(project_id=project_id)
        links_summary = gns3fy.Project(project_id=project_id,connector=gns3_server).links_summary(is_print=False)
        list_of_links=[]
        for link in links:
            for i in link["nodes"]:
                if i["node_id"]==str(node_id):
                    list_of_links.append(i)
        list_of_names=[]
        for l in list_of_links:
            list_of_names.append(l["label"]["text"])
        gns3_server = gns3fy.Gns3Connector("http://localhost:3080")
        node=gns3_server.get_node(project_id=project_id,node_id=node_id)
        ports=[]
        ports=node["ports"]
        to_delete=[]
        print(ports)
        for port in ports:
            for b in list_of_names:
                if port["short_name"]==b:
                    to_delete.append(port)
        print(to_delete)
        for i in to_delete:
            ports.remove(i)
        print(ports)
        return Response(data={"data":ports},status=status.HTTP_200_OK)

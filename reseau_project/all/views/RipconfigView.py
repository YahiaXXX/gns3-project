from ipaddress import ip_address
from pickle import NONE
import telnetlib
from time import sleep
from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from all.serializers.ProjectSerializer import assignipadresssr, ripserializer
import gns3fy


def ripconfig(project_id,node_id,network):
    host = "localhost"
    gns3_server = gns3fy.Gns3Connector("http://localhost:3080")
    node=gns3_server.get_node(project_id=project_id,node_id=node_id)
    #####################################################################
    if node["status"]=="stopped":
        gns3fy.Node(node_id=node_id,project_id=project_id,connector=gns3_server).start()
        sleep(20)
    #####################################################################
    port=node["console"]
    node_name=node["name"]
    #####################################################################
    tn = telnetlib.Telnet(host=host,port=port)
    tn.write(b"\r\n")
    tn.write(b"\r\n")
    tn.write(b"\r\n")
    tn.write(b"\r\n")
    tn.write(b"\r\n")
    tn.write(b"\r\n")
    sleep(1)
    to_file=tn.read_very_eager()
    tn.write(b"conf t\r\n")
    tn.write(b"router rip\r\n")
    tn.write(b"version 2\r\n")
    #####################################################################
    c="network "+str(network)+"\r\n"
    tn.write(c.encode())
    tn.write(b"end\r\n")
    tn.write(b"wr\r\n")
    #####################################################################
    sleep(1)
    t=tn.read_very_eager()
    t=t.decode("utf-8")
    t=t.replace(to_file.decode("utf-8"),"")
    print(t)
    tn.close()
    return t


class RipconfigView(GenericAPIView):
    serializer_class=ripserializer
    #parser_classes = (FormParser, MultiPartParser)
    """"
    defer
    freferf
    frefrefer
    """
    def post(self, request ,project_id,node_id):
        #try: 
            serializer=ripserializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            t=ripconfig(project_id=project_id,node_id=node_id,network=serializer.validated_data['network'])
            return Response(data={"data":t},status=status.HTTP_200_OK)
        #except:
            return Response(data={"notice":"check the gns3 server"},status=status.HTTP_400_BAD_REQUEST)
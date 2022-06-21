from ipaddress import ip_address
from pickle import NONE
import telnetlib
from time import sleep
from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from all.serializers.ProjectSerializer import assignipadresssr
import gns3fy


def assignip(project_id,node_id,interface_name,ip_address,mask):
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
    #####################################################################
    c="int "+str(interface_name)+"\r\n"
    tn.write(c.encode())
    tn.write(b"no shutdown\r\n")
    d="ip address "+str(ip_address)+" "+str(mask)+"\r\n"
    tn.write(d.encode())
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


class AssignIpToIrefaceView(GenericAPIView):
    serializer_class=assignipadresssr
    #parser_classes = (FormParser, MultiPartParser)
    """"
    defer
    freferf
    frefrefer
    """
    def post(self, request ,project_id,node_id):
        #try: 
            serializer=assignipadresssr(data=request.data)
            serializer.is_valid(raise_exception=True)
            t=assignip(project_id=project_id,node_id=node_id,interface_name=serializer.validated_data['interface_name'],ip_address=serializer.validated_data['ip_address'],
            mask=serializer.validated_data['mask'])
            return Response(data={"data":t},status=status.HTTP_200_OK)
        #except:
            return Response(data={"notice":"check the gns3 server"},status=status.HTTP_400_BAD_REQUEST)



from pickle import NONE
import telnetlib
from time import sleep
from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from all.serializers.ProjectSerializer import AddVlanSerializer
import gns3fy



def add_vlan(project_id,node_id,vlan_number,vlan_name):
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
    tn.write(b"enable\n")
    tn.write(b"conf t\n")
    #####################################################################
    c="vlan "+str(vlan_number)+"\n"
    tn.write(c.encode())
    d="name "+str(vlan_name)+"\n"
    tn.write(d.encode())
    tn.write(b"end\n")
    #####################################################################
    sleep(1)
    t=tn.read_very_eager()
    t=t.decode("utf-8")
    t=t.replace(to_file.decode("utf-8"),"")
    print(t)
    a="vIOS-L2-01#"
    t=t.replace(a,"")
    a="vIOS-L2-01>"
    t=t.replace(a,"")
    print(t)
    tn.close()
    return t


class AddVlanView(GenericAPIView):
    serializer_class=AddVlanSerializer
    # parser_classes = (FormParser, MultiPartParser)
    def post(self, request ,project_id,node_id):
        #try: 
            serializer=AddVlanSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            t=add_vlan(project_id=project_id,node_id=node_id,vlan_number=serializer.validated_data['vlan_number'],vlan_name=serializer.validated_data['vlan_name'])
            return Response(data={"data":t},status=status.HTTP_200_OK)
        #except:
            return Response(data={"notice":"check the gns3 server"},status=status.HTTP_400_BAD_REQUEST)

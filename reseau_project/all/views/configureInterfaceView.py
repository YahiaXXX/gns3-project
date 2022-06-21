import telnetlib
from time import sleep
from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from all.serializers.ProjectSerializer import AddVlanSerializer,configureaccess,configuretrunk
import gns3fy
def ConfigureInterfacetrunk(project_id,node_id,interface):
    host = "localhost"
    gns3_server = gns3fy.Gns3Connector("http://localhost:3080")
    node=gns3_server.get_node(project_id=project_id,node_id=node_id)
    print(node["status"])
    if node["status"]=="stopped":
        gns3fy.Node(node_id=node_id,project_id=project_id,connector=gns3_server).start()
        sleep(20)
    port=node["console"]
    node_name=node["name"]
    tn = telnetlib.Telnet(host=host,port=port)
    tn.write(b"\r\n")
    tn.write(b"\r\n")
    tn.write(b"\r\n")
    tn.write(b"\r\n")
    tn.write(b"\r\n")
    tn.write(b"\r\n")
    to_file=tn.read_very_eager()
    with open("reseau_file.txt",'w',encoding = 'utf-8') as f:
        f.write(to_file.decode("utf-8"))
        f.close()
    tn.write(b"enable\r\n")
    tn.write(b"conf t\r\n")
    c="int "+str(interface)+"\r\n"
    tn.write(c.encode())
    tn.write(b"switchport mode trunk\r\n")
    tn.write(b"end\r\n")
    sleep(1)
    t=tn.read_very_eager()
    with open('reseau_file.txt', 'rb') as file:
        data = file.read()
    t=t.decode("utf-8")
    t=t.replace(data.decode("utf-8"),"")
    print(t)
    tn.close()
    return t





def ConfigureInterfaceaccess(project_id,node_id,interface,vlan_number):
    host = "localhost"
    gns3_server = gns3fy.Gns3Connector("http://localhost:3080")
    node=gns3_server.get_node(project_id=project_id,node_id=node_id)
    print(node["status"])
    if node["status"]=="stopped":
        gns3fy.Node(node_id=node_id,project_id=project_id,connector=gns3_server).start()
    port=node["console"]
    node_name=node["name"]
    print(node_name)
    print(port)
    tn = telnetlib.Telnet(host=host,port=port)
    tn.write(b"\r\n")
    tn.write(b"\r\n")
    tn.write(b"\r\n")
    tn.write(b"enable\r\n")
    tn.write(b"conf t\r\n")
    c="int "+str(interface)+"\r\n"
    tn.write(c.encode())
    tn.write(b"switchport mode access\r\n")
    d="switchport access vlan "+str(vlan_number)+"\r\n"
    tn.write(d.encode())
    tn.write(b"end\r\n")
    sleep(1)
    t=tn.read_very_eager()
    print(t.decode("utf-8"))
    tn.close()
    return t.decode("utf-8")


class ConfigureAccessView(GenericAPIView):
    serializer_class=configureaccess
    # parser_classes = (FormParser, MultiPartParser)
    def post(self, request ,project_id,node_id):
        try: 
            serializer=configureaccess(data=request.data)
            serializer.is_valid(raise_exception=True)
            t=ConfigureInterfaceaccess(project_id=project_id,node_id=node_id,vlan_number=serializer.validated_data['vlan_number'],interface=serializer.validated_data['interface_name'])
            return Response(data={"data":t},status=status.HTTP_200_OK)
        except:
            return Response(data={"notice":"check the gns3 server"},status=status.HTTP_400_BAD_REQUEST)


class ConfigureTrunkView(GenericAPIView):
    serializer_class=configuretrunk
    # parser_classes = (FormParser, MultiPartParser)
    def post(self, request ,project_id,node_id):
        #try: 
            serializer=configuretrunk(data=request.data)
            serializer.is_valid(raise_exception=True)
            t=ConfigureInterfacetrunk(project_id=project_id,node_id=node_id,interface=serializer.validated_data['interface_name'])
            return Response(data={"data":t},status=status.HTTP_200_OK)
        #except:
            return Response(data={"notice":"check the gns3 server"},status=status.HTTP_400_BAD_REQUEST)
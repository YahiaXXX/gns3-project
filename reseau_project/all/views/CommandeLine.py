
from asyncore import read, write
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

from all.serializers.ProjectSerializer import commandesr


def commandeline(project_id,node_id,commande):
    host = "localhost"
    gns3_server = gns3fy.Gns3Connector("http://localhost:3080")
    node=gns3_server.get_node(project_id=project_id,node_id=node_id)
    #######################################################################
    if node["status"]=="stopped":
        gns3fy.Node(node_id=node_id,project_id=project_id,connector=gns3_server).start()
        sleep(30)
    #######################################################################
    port=node["console"]
    node_name=node["name"]
    tn = telnetlib.Telnet(host=host,port=port)
    tn.write(b"\r\n")
    tn.write(b"\r\n")
    tn.write(b"\r\n")
    tn.write(b"\r\n")
    tn.write(b"\r\n")
    tn.write(b"\r\n")
    tn.write(b"enable\r\n")
    sleep(1)
    to_file=tn.read_very_eager()
    #######################################################################
    c=str(commande)+"\r\n"
    tn.write(c.encode())
    sleep(1)
    for i in range(0,150):
        tn.write(b"\r\n")
    if gns3_server.get_template(template_id=node["template_id"])["category"]=="router":
        sleep(2)
    else:
        sleep(2)
    #tn.read_until(b"vIOS-L2-01#")
    t=tn.read_very_eager()
    t=t.decode("utf-8")
    t=t.replace(to_file.decode("utf-8"),"")
    a="vIOS-L2-01#"
    t=t.replace(a,"")
    a="vIOS-L2-01>"
    t=t.replace(a,"")
    a="R1#"
    t=t.replace(a,"")
    if gns3_server.get_template(template_id=node["template_id"])["category"]=="router":
        t=t.replace(a,"")
        t=t.replace("--More-- \b\b\b\b\b\b\b\b\b","")
        t=t.replace("\b\b\b\b\b\b\b\b\b","")
        t=t.replace("         ","")
        print(t)
        t=t[0:t.rfind("end")+4]
        t=t.split("\r\n")
        
    else:
        print(t)
    tn.close()
    return t

class CommandeLine(GenericAPIView):
    serializer_class=commandesr
    #parser_classes = (FormParser, MultiPartParser)
    def post(self, request ,project_id,node_id):
        #try: 
            serializer=commandesr(data=request.data)
            serializer.is_valid(raise_exception=True)
            t=commandeline(project_id=project_id,node_id=node_id,commande=serializer.validated_data['commande'])
            return Response(data={"data":t},status=status.HTTP_200_OK)
        #except:
            return Response(data={"notice":"check the gns3 server"},status=status.HTTP_400_BAD_REQUEST)
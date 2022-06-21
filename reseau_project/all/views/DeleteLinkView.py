

from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from all.serializers.ProjectSerializer import DeleteLinkSerializer
import gns3fy

def delete_link(project_id,node_1_name,node_2_name):
    gns3_server = gns3fy.Gns3Connector("http://localhost:3080")
    links_summary=gns3_server.get_links(project_id=project_id)
    node_a=gns3fy.Node(name=node_1_name,project_id=project_id,connector=gns3_server)
    node_a.get()
    node_a_id=node_a.node_id
    node_b=gns3fy.Node(name=node_2_name,project_id=project_id,connector=gns3_server)
    node_b.get()
    node_b_id=node_b.node_id
    print(links_summary)
    for link in links_summary:
        print(link['nodes'][0]["node_id"])
        print(link['nodes'][1]["node_id"])
        if(link['nodes'][0]["node_id"]==node_a_id and link['nodes'][1]["node_id"]==node_b_id):
            link=gns3fy.Link(link_id=link["link_id"],project_id=project_id,connector=gns3_server)
            link.get()
            link.delete()

class DeleteLinkView(GenericAPIView):
    """
    """
    serializer_class=DeleteLinkSerializer
    # parser_classes = (FormParser, MultiPartParser)
    def post(self, request ,project_id):
        # try:
            serializer=DeleteLinkSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            delete_link(project_id=project_id,node_1_name=serializer.validated_data['node_1_name'],node_2_name=serializer.validated_data['node_2_name'])
            return Response(status=status.HTTP_200_OK)
        # except:
            return Response(data={"notice":"check the gns3 server"},status=status.HTTP_400_BAD_REQUEST)

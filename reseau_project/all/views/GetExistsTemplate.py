
from email.policy import default
from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from all.serializers.ProjectSerializer import ProjectSerializer
import gns3fy

class GetExistsTemplates(GenericAPIView):
    """get
    get all the templates  exists en the server (routers , switchs, vpcs)
    """
    parser_classes = (FormParser, MultiPartParser)
    def get(self, request):
            gns3_server = gns3fy.Gns3Connector("http://localhost:3080")
            templates=gns3_server.get_templates()
            for l in templates :
                l.pop("auto_delete_disks",None)
                l.pop("console_auto_start",None)
                l.pop("console_type",None)
                l.pop("default_name_format",None)
                l.pop("disk0",None)
                l.pop("disk1",None)
                l.pop("exec_area",None)
                l.pop("idlemax",None)
                l.pop("console_type",None)
                l.pop("idlesleep",None)
                l.pop("iomem",None)
                l.pop("mac_addr",None)
                l.pop("mmap",None)
                l.pop("slot0",None)
                l.pop("console_type",None)
                l.pop("private_config",None)
                l.pop("sparsemem",None)
                l.pop("slot1",None)
                l.pop("slot2",None)
                l.pop("slot3",None)
                l.pop("usage",None)
                l.pop("idlepc",None)
                l.pop("midplane",None)
                l.pop("npe",None)
                l.pop("usage",None)
            return Response(data=templates,status=status.HTTP_200_OK)

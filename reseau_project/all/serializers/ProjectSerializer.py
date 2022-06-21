from email.policy import default
from pyexpat import model
from re import template
from rest_framework import serializers

class ProjectSerializer(serializers.Serializer):
    name=serializers.CharField()

class Nodeserializer(serializers.Serializer):
    template=serializers.CharField()

class linkserializer(serializers.Serializer):
    node_id_1=serializers.CharField()
    node_id_1_adapter_number=serializers.IntegerField()
    node_id_1_port_number=serializers.IntegerField()
    node_id_2=serializers.CharField()
    node_id_2_adapter_number=serializers.IntegerField()
    node_id_2_port_number=serializers.IntegerField()

class DeleteLinkSerializer(serializers.Serializer):
    node_1_name=serializers.CharField()
    node_2_name=serializers.CharField()

class AddVlanSerializer(serializers.Serializer):
    vlan_name=serializers.CharField()
    vlan_number=serializers.IntegerField()

class configuretrunk(serializers.Serializer):
    interface_name=serializers.CharField()

class configureaccess(serializers.Serializer):
    interface_name=serializers.CharField()
    vlan_number=serializers.IntegerField()
class commandesr(serializers.Serializer):
    commande=serializers.CharField()

class assignipadresssr(serializers.Serializer):
    interface_name=serializers.CharField()
    ip_address=serializers.IPAddressField()
    mask=serializers.IPAddressField()

class ripserializer(serializers.Serializer):
    network=serializers.IPAddressField()

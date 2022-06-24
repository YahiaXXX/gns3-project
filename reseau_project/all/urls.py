
from django.urls import path
from requests import delete

from all.views.RipconfigView import RipconfigView
from .views.ProjectsViews import ProjectsViews , GetProjectWithIdViews
from .views.GetExistsTemplate import GetExistsTemplates
from .views.GetExistsTemplateWithid import GetExistsTemplateWithid
from .views.ProjectNodesView import ProjectNodesView
from .views.ProjectLinksView import ProjectLinksView
from .views.DeleteLinkView import DeleteLinkView
from .views.AddVlanView import AddVlanView
from .views.CommandeLine import CommandeLine
from .views.configureInterfaceView import ConfigureAccessView, ConfigureTrunkView
from .views.AssignIpToIrefaceView import AssignIpToIrefaceView
from .views.GetInterfacesView import GetInterfacesView
from .views.openprojectview import openprojectview , closeprojetview
from .views.deletenode import deletenode
urlpatterns = [
    path('delete/node/<slug:project_id>/<slug:node_id>',deletenode.as_view()),
    path('',ProjectsViews.as_view()),
    path('<slug:project_id>',GetProjectWithIdViews.as_view()),
    path('open/<slug:project_id>',openprojectview.as_view()),
    path('close/<slug:project_id>',closeprojetview.as_view()),
    path('/link/delete/<slug:project_id>',DeleteLinkView.as_view()),
    path('templates/all',GetExistsTemplates.as_view()),
    path('templates/<slug:template_id>',GetExistsTemplateWithid.as_view()),
    path('nodes/<slug:project_id>',ProjectNodesView.as_view()),
    path('nodes/interfaces/<slug:project_id>/<slug:node_id>',GetInterfacesView.as_view()),
    path('links/<slug:project_id>',ProjectLinksView.as_view()),
    path('switch/add_vlan/<slug:project_id>/<slug:node_id>',AddVlanView.as_view()),
    path('switch/configure_interface_access/<slug:project_id>/<slug:node_id>',ConfigureAccessView.as_view()),
    path('switch/configure_interface_trunk/<slug:project_id>/<slug:node_id>',ConfigureTrunkView.as_view()),
    path('commandeline/<slug:project_id>/<slug:node_id>',CommandeLine.as_view()),
    path('router/assign_ip_to_interface/<slug:project_id>/<slug:node_id>',AssignIpToIrefaceView.as_view()),
    path('router/rip_config/<slug:project_id>/<slug:node_id>',RipconfigView.as_view()),
    
]
"""    path('switch/add_vlan/<slug:project_id>',ProjectLinksView.as_view()),
    path('switch/configure_interface/<slug:project_id>',ProjectLinksView.as_view()),
    path('router/configure_ip/<slug:project_id>',ProjectLinksView.as_view()),
    path('router/configure_rip/<slug:project_id>',ProjectLinksView.as_view()),
    path('show_runnig_config/<slug:project_id>',ProjectLinksView.as_view()),"""
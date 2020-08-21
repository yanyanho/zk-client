
from django.conf.urls import url

from . import views
from . import routes

 

 

urlpatterns = [
    #url(r'^genFiscoAddr$', routes.genFiscoAddr),
    url(r'^genZbacAddr$', routes.genZbacAddr),
    url(r'^deployToken$', routes.deployToken),
    url(r'^deployMixer$', routes.deployMixer),
    url(r'^depositBac$', routes.depositBac),
    url(r'^mixBac$', routes.mixBac),
    url(r'^sendAsset$', routes.sendAsset),
    url(r'^getNotes$', routes.getNotes),
    url(r'^importFiscoAddr$', routes.importFiscoAddr),
    #url(r'^getCommits$', routes.getCommits),
    url(r'^checkUser$', routes.checkUser),
    url(r'^genAccount$', routes.genAccount),
    #url(r'^getBacContract$', routes.getBacContract),
    #url(r'^getMixerContract$', routes.getMixerContract),
    url(r'^getTransactions$', routes.getTransactions),
    url(r'^getContract$', routes.getContract),
    url(r'^getBalance$', routes.getBalance),
]

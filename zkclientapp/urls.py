
from django.conf.urls import url

from . import views
from . import routes

 

 

urlpatterns = [

    #主页

    url(r'^$',views.index,name='index'),
    url(r'^get\.html$', views.get_html),
    url(r'^get$', views.get),
    url(r'^post\.html$', views.post_html),
    url(r'^post$', views.post),
    url(r'^genFiscoAddr$', routes.genFiscoAddr),
    url(r'^genZbacAddr$', routes.genZbacAddr),
    url(r'^deployToken$', routes.deployToken),
    url(r'^deployMixer$', routes.deployMixer),
    url(r'^depositBac$', routes.depositBac),
]

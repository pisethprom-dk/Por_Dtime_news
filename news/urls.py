from django.conf.urls import url
from .views import ( CategoryView, CategoryDetailView, MenuView, MenuDetailView,
                     NewsView, NewsDetailView, AddNewsView, ParentMenu,
                     SlideNewsView, RelateNewsView, PorpularNewView )

urlpatterns = [
    url(r'^$', NewsView.as_view(), name='news'),
    url(r'^related-news/$', RelateNewsView.as_view(), name='related news'),
    url(r'^porpular-news/$', PorpularNewView.as_view(), name='porpular news'),
    url(r'^slide-news/$', SlideNewsView.as_view(), name='slide news'),
    url(r'^(?P<pk>\d+)/$', NewsDetailView.as_view(), name='news news detail'),
    url(r'^post/$', AddNewsView.as_view(), name='add news'),
    url(r'^category/$', CategoryView.as_view(), name='news category'),
    url(r'^category/(?P<pk>\d+)/$', CategoryDetailView.as_view(), name='news category detail'),
    url(r'^menu/$', MenuView.as_view(), name='news menu'),
    url(r'^parent_menu/$', ParentMenu.as_view(), name='news parent menu'),
    url(r'^menu/(?P<pk>\d+)/$', MenuDetailView.as_view(), name='news menu detail'),
]
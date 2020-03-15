from django.conf.urls import url
from .views import ( UserProfileView, UserManageView, UserRoleView, UserView,
                   UserPickCategoriesView, SaveNewsView, DetailSaveNewsView, ListSaveNewsView)
urlpatterns = [
    url(r'^$', UserProfileView.as_view(), name = 'user_profile'),
    url(r'^role/$', UserRoleView.as_view(), name = 'user_role'),
    url(r'^list/$', UserView.as_view(), name = 'list_user'),
    url(r'^manage/(?P<pk>\d+)/$', UserManageView.as_view(), name='user_detail'),
    url(r'^pick-category/$', UserPickCategoriesView.as_view(), name='user_pick_categories'),
    url(r'^save-news/$', SaveNewsView.as_view(), name='save news'),
    url(r'^save-news/(?P<pk>\d+)/$', DetailSaveNewsView.as_view(), name='detail new'),
    url(r'^list-saved-news/$', ListSaveNewsView.as_view(), name='list saved news'),
    # url(r'^total_user/$', TotalUser.as_view(), name = 'total_user'),
]
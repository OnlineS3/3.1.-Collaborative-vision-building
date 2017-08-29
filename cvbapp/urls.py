from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='cvbapp_index'),
	url(r'^about$', views.about, name='cvbapp_about'),
	url(r'^guide$', views.guide, name='cvbapp_guide'),
	url(r'^related$', views.related, name='cvbapp_related'),
	url(r'^login$', views.login_view, name='cvbapp_loginview'),
	url(r'^logoutview$', views.logout, name='cvbapp_logoutview'),
	url(r'^createsession$', views.create_visionsession, name='cvbapp_createsession'),
	url(r'^deletesession$', views.delete_vision_session, name='cvbapp_deletesession'),
	url(r'^getsessions$', views.get_visionsessions, name='cvbapp_getsessions'),
	url(r'^visionprofile$', views.get_vision_profile, name='cvbapp_visionprofile'),
	url(r'^editvisionprofile$', views.edit_vision_profile, name='cvbapp_editvisionprofile'),
	url(r'^updatevisionprofile$', views.update_vision_profile, name='cvbapp_updatevisionprofile'),
	url(r'^searchsessions$', views.search_sessions, name='cvbapp_searchsessions'),
	url(r'^createstatement$', views.create_vision_statement, name='cvbapp_createstatement'),
	url(r'^getstatement$', views.get_vision_statement, name='cvbapp_getstatement'),
	url(r'^getstatements$', views.get_vision_statements, name='cvbapp_getstatements'),
	url(r'^getchannelusercount$', views.get_channel_user_count, name='cvbapp_getchannelusercount'),
	url(r'^getchannelhistory$', views.get_channel_history, name='cvbapp_getchannelhistory'),
	url(r'^createscheduledmeeting$', views.create_scheduled_meeting, name='cvbapp_createscheduledmeeting'),
	url(r'^createvisionreport$', views.create_vision_report, name='cvbapp_createvisionreport'),
	url(r'^exporttopdf$', views.export_to_pdf, name='cvbapp_exporttopdf'),
	url(r'^callback$', views.callback, name='cvbapp_callback'),
	url(r'^access$', views.callback, name='cvbapp_access')
]
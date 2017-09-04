from django.shortcuts import render,redirect
import json
from django.http import HttpResponse, FileResponse
import requests
import pdfkit

#from weasyprint import HTML, CSS

from auth0.v3.authentication import GetToken
from auth0.v3.authentication import Users

from .models import VisionSession,VisionStatement,Channel,ScheduledMeeting,VisionReport

rocketchat_url = "http://li1088-54.members.linode.com:3000"
rocketchat_user = "admin"
rocketchat_pass = "buffalobrotherbreakfastproduct"

client_id = "dxWIFs8VoxLcqNkSbqVOCbPn3auoFzfa"
client_secret = "IWtoIeh279Q6gG_nPtGV3pgc3gB_HPhtwT5pk6hrqCScv22Zv-AZd-GlE3hH6XpC"

def index(request):
	context = {}
	if 'delete_success' in request.session:
		context['delete_success'] = request.session['delete_success']
		request.session.pop('delete_success', None)
	else:
		context['delete_success'] = None
	return render(request, 'cvbapp/index.html', context=context)


def guide(request):
	return render(request, 'cvbapp/guide.html')

def about(request):
	return render(request, 'cvbapp/about.html')

def access(request):
	return render(request, 'cvbapp/access_app.html')

def related(request):
	return render(request, 'cvbapp/related_documents.html')


def login_view(request):
	request.session['cvbapp_profile'] = json.loads( '{"email": "' + request.POST['username'] + '", "nickname": "' + request.POST['username'] + '"}')
	return redirect('cvbapp_index')


def logout_view(request):
	request.session['cvbapp_profile'] = None
	return redirect('cvbapp_index')


def create_visionsession(request):
	if VisionSession.objects.filter(session_name=request.POST['session_name'].replace(" ", "")).count() == 0:
		r = requests.post(rocketchat_url+'/api/v1/login', data={'username': rocketchat_user, 'password': rocketchat_pass})
		j = json.loads(r.text)
		r = requests.post(rocketchat_url+'/api/v1/channels.create', auth=(rocketchat_user, rocketchat_pass),
						  data={'name': request.POST['session_name'].replace(" ", "")},
						  headers={'X-Auth-Token': j['data']['authToken'], 'X-User-Id': j['data']['userId']})
		print(r.text)
		j = json.loads(r.text)

		channel_instance = Channel.objects.create(room_id=j["channel"]["_id"], channel_name=j["channel"]["name"], rc_channel=rocketchat_url+'/channel/' + request.POST['session_name'].replace(" ", ""))

		visionsession_instance = VisionSession.objects.create(user_email=request.session['cvbapp_profile']['nickname'],session_name=request.POST['session_name'],session_description=request.POST['session_description'],phase=2, channel=channel_instance)
		visionsession_instance.save()
		return redirect('cvbapp_index')
	else:
		return HttpResponse('a session with that name already exists', status="409")


def delete_vision_session(request):
	session_name = request.POST['session_name']
	visionsession_instance = VisionSession.objects.filter(session_name=session_name)

	r = requests.post(rocketchat_url+'/api/v1/login', data={'username': rocketchat_user, 'password': rocketchat_pass})
	j = json.loads(r.text)
	r = requests.post(rocketchat_url+'/api/v1/channels.delete', auth=(rocketchat_user, rocketchat_pass),
					  data={'roomId': visionsession_instance[0].channel.room_id},
					  headers={'X-Auth-Token': j['data']['authToken'], 'X-User-Id': j['data']['userId']})
	print(r.text)
	j = json.loads(r.text)

	visionsession_instance[0].delete()
	request.session['delete_success']='true';
	return redirect('cvbapp_index')


def get_visionsessions(request):
	visionsessions = VisionSession.objects.all()
	data = {}
	data['sessions'] = []
	for vs in visionsessions:
		session = {}
		session['user_email'] = vs.user_email
		session['session_name'] = vs.session_name
		session['session_description'] = vs.session_description
		data['sessions'].append(session)
	j = json.dumps(data)
	return HttpResponse(j)


def get_vision_profile(request):
	session_name = request.GET['session_name']
	visionsession_instance = VisionSession.objects.filter(session_name=session_name)

	submitted_statement_p2 = ""
	if VisionStatement.objects.filter(user_email=request.session['cvbapp_profile']['nickname'], session=visionsession_instance, phase=2).count() > 0:
		submitted_statement_p2 = VisionStatement.objects.filter(user_email=request.session['cvbapp_profile']['nickname'],
									session=visionsession_instance, phase=2)[0].vision_statement

	submitted_statement_p3 = ""
	if VisionStatement.objects.filter(user_email=request.session['cvbapp_profile']['nickname'],
									  session=visionsession_instance, phase=3).count() > 0:
		submitted_statement_p3 = VisionStatement.objects.filter(user_email=request.session['cvbapp_profile']['nickname'],
									session=visionsession_instance, phase=3)[0].vision_statement

	submitted_statement_p5 = ""
	if VisionStatement.objects.filter(user_email=request.session['cvbapp_profile']['nickname'],
									  session=visionsession_instance, phase=5).count() > 0:
		submitted_statement_p5 = VisionStatement.objects.filter(user_email=request.session['cvbapp_profile']['nickname'],
									session=visionsession_instance, phase=5)[0].vision_statement
		print "p5: " + submitted_statement_p5
	print "p5: " + submitted_statement_p5

	submitted_meeting_p4 = ""
	if ScheduledMeeting.objects.filter(channel = visionsession_instance[0].channel, phase=4).count() > 0:
		submitted_meeting_p4 = ScheduledMeeting.objects.filter(channel = visionsession_instance[0].channel, phase=4)[0].datetime

	submitted_report = ""
	if VisionReport.objects.filter(session=visionsession_instance[0]).count() > 0:
		submitted_report = VisionReport.objects.filter(session=visionsession_instance[0])[0].vision_report

	context = {"session_name":session_name,
			   "session_description": visionsession_instance[0].session_description,
			   "user_email": visionsession_instance[0].user_email,
			   "phase": visionsession_instance[0].phase,
			   "rc_channel": visionsession_instance[0].channel.rc_channel,
			   "submitted_statement_p2": submitted_statement_p2,
			   "submitted_statement_p3": submitted_statement_p3,
			   "submitted_statement_p5": submitted_statement_p5,
			   "submitted_meeting_p4": submitted_meeting_p4,
			   "submitted_report": submitted_report}
	return render(request, 'cvbapp/visionprofile.html', context)


def edit_vision_profile(request):
	session_name = request.GET['session_name']
	visionsession_instance = VisionSession.objects.filter(session_name=session_name)
	context = {"session_name":session_name, "session_description": visionsession_instance[0].session_description, "user_email": visionsession_instance[0].user_email}
	return render(request, 'cvbapp/editvisionprofile.html', context)


def update_vision_profile(request):
	session_name = request.POST['old_session_name']
	visionsession_instance = VisionSession.objects.get(session_name=session_name)
	if 'session_name' in request.POST:
		visionsession_instance.session_name = request.POST['session_name']
	if 'session_description' in request.POST:
		visionsession_instance.session_description = request.POST['session_description']
	if 'phase_advance' in request.POST:
		visionsession_instance.phase += 1
	if 'phase_decrease' in request.POST:
		visionsession_instance.phase -= 1
	visionsession_instance.save()
	return redirect(request.POST['redirect_url']+'?session_name=' + (request.POST['session_name'] if 'session_name' in request.POST else 'null') +
					"&session_description=" + (request.POST['session_description'] if 'session_description' in request.POST else 'null'))


def search_sessions(request):
	searchterm = request.GET['searchterm']
	visionsessions_str = ""
	data = {}
	data['sessions'] = []
	if request.GET['searchtype'] == "Name" or request.GET['searchtype'] == "All":
		visionsessions = VisionSession.objects.filter(session_name__contains=searchterm)
		for vs in visionsessions:
			session = {}
			session['user_email'] = vs.user_email
			session['session_name'] = vs.session_name
			session['session_description'] = vs.session_description
			if not session in data['sessions']:
				data['sessions'].append(session)
			print vs.session_name
	if request.GET['searchtype'] == "Description" or request.GET['searchtype'] == "All":
		visionsessions = VisionSession.objects.filter(session_description__contains=searchterm)
		for vs in visionsessions:
			session = {}
			session['user_email'] = vs.user_email
			session['session_name'] = vs.session_name
			session['session_description'] = vs.session_description
			if not session in data['sessions']:
				data['sessions'].append(session)
	j = json.dumps(data)
	return HttpResponse(j)


def create_vision_statement(request):
	vision_session_instance = VisionSession.objects.get(session_name=request.POST['session_name'])

	if VisionStatement.objects.filter(user_email=request.session['cvbapp_profile']['nickname'],session=vision_session_instance,phase=request.POST['phase']).count() >0:
		#edit statement
		print request.POST['phase']
		vision_statement_instance = VisionStatement.objects.get(user_email=request.session['cvbapp_profile']['nickname'],session=vision_session_instance,phase=request.POST['phase'])
		vision_statement_instance.vision_statement = request.POST['vision_statement']
		vision_statement_instance.save()
	else:
		#create new
		print request.POST['phase']
		vision_statement_instance = VisionStatement.objects.create(session=vision_session_instance,
																   user_email=request.session['cvbapp_profile']['nickname'],
																   vision_statement=request.POST['vision_statement'],
																   phase=request.POST['phase'])
		vision_statement_instance.save()
	return HttpResponse('OK')


def get_vision_statement(request):
	vision_session_instance = VisionSession.objects.get(session_name=request.GET['session_name'])
	vision_statement_instance = VisionStatement.objects.get(user_email=request.session['cvbapp_profile']['nickname'], session=vision_session_instance,phase=request.GET['phase'])
	return HttpResponse(vision_statement_instance.vision_statement)


def get_vision_statements(request):
	vision_session_instance = VisionSession.objects.get(session_name=request.GET['session_name'])
	vision_statements = VisionStatement.objects.filter(session=vision_session_instance,phase=request.GET['phase'])
	data = {}
	data['statements'] = []
	for vs in vision_statements:
		data['statements'].append(vs.vision_statement)
	j = json.dumps(data)
	return HttpResponse(j)


def get_channel_user_count(request):
	session_name = request.GET['session_name']
	visionsession_instance = VisionSession.objects.get(session_name=session_name)

	r = requests.post(rocketchat_url+'/api/v1/login', data={'username': rocketchat_user, 'password': rocketchat_pass})
	j = json.loads(r.text)
	r = requests.get(rocketchat_url+'/api/v1/channels.info', params={'roomName': visionsession_instance.channel.channel_name},
					 headers={'X-Auth-Token': j['data']['authToken'], 'X-User-Id': j['data']['userId']})
	j = json.loads(r.text)
	print r.text
	return HttpResponse(len(j['channel']['usernames']))


def get_channel_history(request):
	session_name = request.GET['session_name']
	visionsession_instance = VisionSession.objects.get(session_name=session_name)

	#log in user
	r = requests.post(rocketchat_url+'/api/v1/login', data={'username': rocketchat_user, 'password': rocketchat_pass})
	user_json = json.loads(r.text)
	#get channel info
	r = requests.get(rocketchat_url+'/api/v1/channels.info', params={'roomName': visionsession_instance.channel.channel_name},
					 headers={'X-Auth-Token': user_json['data']['authToken'], 'X-User-Id': user_json['data']['userId']})
	channel_json = json.loads(r.text)
	#get channel history
	r = requests.get(rocketchat_url+'/api/v1/channels.history', params={'roomId': channel_json["channel"]["_id"], "unreads": "true"},
					 headers={'X-Auth-Token': user_json['data']['authToken'], 'X-User-Id': user_json['data']['userId']})
	history_json = json.loads(r.text)
	return HttpResponse(r.text)


def create_scheduled_meeting(request):
	vision_session_instance = VisionSession.objects.get(session_name=request.POST['session_name'])
	datetime = request.POST['date']+'-'+request.POST['hour']+':'+request.POST['minute']
	scheduled_meeting_instance = ScheduledMeeting.objects.create(channel=vision_session_instance.channel, datetime=datetime, phase=request.POST['phase'])
	scheduled_meeting_instance.save()
	return HttpResponse('OK')


def create_vision_report(request):
	vision_session_instance = VisionSession.objects.get(session_name=request.POST['session_name'])
	if VisionReport.objects.filter(session=vision_session_instance).count() > 0:
		vision_report_instance = VisionReport.objects.get(session=vision_session_instance)
		vision_report_instance.vision_report = request.POST['report']
		vision_report_instance.save()
		return HttpResponse('OK')
	else:
		vision_report_instance = VisionReport.objects.create(session=vision_session_instance, vision_report=request.POST['report'])
		vision_report_instance.save()
		return HttpResponse('OK')


def export_to_pdf(request):
	#pdf = HTML(string=request.POST['html_string']).write_pdf(stylesheets=[CSS(filename="/home/django/balancedscorecard/cvbapp/static/css/cvb.css"), CSS(filename="/home/django/balancedscorecard/cvbapp/static/css/layout.css")])

	html_string = request.POST['html_string']
	config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
	css = [
		'C:\\Users\\Joel Potts\\PycharmProjects\\onlines3_django\\cvbapp\\static\\css\\cvb.css',
		'C:\\Users\\Joel Potts\\PycharmProjects\\onlines3_django\\cvbapp\\static\\css\\layout.css',
	]
	pdf = pdfkit.from_string(html_string, False, configuration=config, css=css)
	#pdfkit.from_file('C:\\Users\\Joel Potts\\Documents\\Online S3\\WP4\\SWOT\\SWOT v4\\related_documents.html', 'out.pdf', configuration=config, css=css)
	response = FileResponse(pdf, content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename=swot_analysis.pdf'
	return response
	#return FileResponse(pdf, content_type='application/pdf')

def callback(request):
	code = request.GET['code']
	get_token = GetToken('onlines3.eu.auth0.com')
	auth0_users = Users('onlines3.eu.auth0.com')
	token = get_token.authorization_code(client_id, client_secret, code, 'http://li1088-54.members.linode.com:8082/cvbapp/callback/')
	user_info = auth0_users.userinfo(token['access_token'])
	request.session['cvbapp_profile'] = json.loads(user_info)
	#save user to db and session
	return redirect('cvbapp_index')

def logout(request):
	request.session['cvbapp_profile'] = None
	#parsed_base_url = urlparse('http://li1088-54.members.linode.com:8082/bscapp/callback/')
	#base_url = parsed_base_url.scheme + '://' + parsed_base_url.netloc
	#return redirect('https://%s/v2/logout?returnTo=%s&client_id=%s' % ('onlines3.eu.auth0.com', base_url, 'vE0hJ4Gx1uYG9LBtuxgqY7CTIFmKivFH'))
	return redirect('cvbapp_index')


$( document ).ready(function() {
	var auth = new auth0.WebAuth({
		domain: 'onlines3.eu.auth0.com',
		clientID: 'dxWIFs8VoxLcqNkSbqVOCbPn3auoFzfa'
	});

	$('.login-btn').click(function(e) {
    	console.log("testing");
      e.preventDefault();
      auth.authorize({
        audience: 'https://' + 'onlines3.eu.auth0.com' + '/userinfo',
        scope: 'openid profile email',
        responseType: 'code',
        redirectUri: 'http://li1088-54.members.linode.com:8082/cvbapp/callback'
      });
    });
    $('.register-btn').click(function(e) {
      e.preventDefault();
      auth.authorize({
        audience: 'https://' + 'onlines3.eu.auth0.com' + '/userinfo',
        scope: 'openid profile email',
        responseType: 'code',
        redirectUri: 'http://li1088-54.members.linode.com:8082/cvbapp/callback'
      });
    });

    // Close the dropdown menu if the user clicks outside of it
    // window.onclick = function(event) {
		// if (!event.target.matches('.dropbtn')) {
		// 	$('.dropdown-content:visible').toggle();
		// }
    // }

	$('.js-example-basic-single').select2();

	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
		 function getCookie(name) {
			 var cookieValue = null;
			 if (document.cookie && document.cookie != '') {
				 var cookies = document.cookie.split(';');
				 for (var i = 0; i < cookies.length; i++) {
					 var cookie = jQuery.trim(cookies[i]);
					 // Does this cookie string begin with the name we want?
					 if (cookie.substring(0, name.length + 1) == (name + '=')) {
						 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
						 break;
					 }
				 }
			 }
			 return cookieValue;
		 }
		 if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
			 // Only send the token to relative URLs i.e. locally.
			 xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
		 }
		}
	});

	var tour = new Tour({
		backdrop:"true",
		onEnd: function (tour) {
			window.location = document.getElementById("tool").getAttribute("href");
			if(document.getElementById("visionsession_list"))
			{
				getSessions();
			}
		},
		steps: [
			{
				element: "#userbtns",
				title: "Sign in",
				content: "Sign in or Sign up to gain full access to the app",
			},
			{
				element: "#searchdiv",
				title: "Search bar",
				content: "Use the search to search for and filter vision sessions"
			},
			{
				element: "#createbtn",
				title: "Create Button",
				content: "Use the create button to create new vision sessions"
			},
			{
				element: "#button_div",
				title: "Access Button",
				content: "Use this button to access a vision session"
			},
			{
				element: "#phase_1",
				title: "Session Info",
				content: "This section provides some information about the session",
				path: "/cvbapp/demo"
			},
			{
				element: "#phase2",
				title: "Step 2",
				content: "In this step the initial Vision Statements are suggested",
			},
			{
				element: "#phase3",
				title: "Step 3",
				content: "In this step the owner of the Session will use the suggested statements to create a single draft statement",
			},
			{
				element: "#phase4",
				title: "Step 4",
				content: "In this step a live chat is organized and held, in order to discuss any changes that should be made to the vision statement",
			},
			{
				element: "#phase5",
				title: "Step 5",
				content: "In this step the owner of the session will create a final vision statement and create a short report on their decisions",
			},
			{
				element: "#phase6",
				title: "Step 6",
				content: "This step shows the final results of the Vision Building process and provides a summary report as a PDF",
			}
		]
	});
	tour.init();
	tour.start();

	if(tour.ended() && document.getElementById("created_visionsession_list"))
	{
		getSessions();
	}
});

$(".form_datetime").datetimepicker({
	format: "dd MM yyyy - hh:ii"
});

function createSession()
{
	$.ajax({url: document.getElementById("session_create_button").getAttribute("action"),
			type: "POST",
			data: {
				session_name: document.getElementById("session_name_input").value,
                session_description: document.getElementById("session_description_input").value,
				region: $("#region_input").select2("val"),
				private: document.getElementById('session_private').checked?'True':'False'
			},
			success: function(result){
				console.log("success: " + result);
				createModalNotification("Notification", document.getElementById("session_name_input").value + " created successfully.");
				getSessions();
			},
			error: function(xhr, status, error){
				console.log("xhr: " + xhr.responseText);
				console.log("status: " + status);
				console.log("error: " + error);
			}
	});
	$('#session_private').attr('checked',false);
	$('#session_name_input').val('');
	$('#session_description_input').val('');
}

function joinSession()
{
	$.ajax({url: document.getElementById("share_id_button").getAttribute("action"),
			type: "POST",
			data: {
				share_id: document.getElementById("share_id_input").value
			},
			success: function(result){
				console.log("success: " + result);
				createModalNotification("Notification", document.getElementById("session_name_input").value + " joined successfully.");
				getSessions();
			},
			error: function(xhr, status, error){
				console.log("xhr: " + xhr.responseText);
				console.log("status: " + status);
				console.log("error: " + error);
			}
	});
}

function getSessions()
{
	$.ajax({url: document.getElementById("created_visionsession_list").getAttribute("action"),
			type: "GET",
			success: function(result){
				console.log("success: " + result);
				clearSessions();
				loadSessions(result);
			},
			error: function(xhr, status, error){
				console.log("xhr: " + xhr.responseText);
				console.log("status: " + status);
				console.log("error: " + error);
			}
	});
}

function searchSessions()
{
	if(document.getElementById("dropdown_selection").innerHTML == "Region")
	{
		document.getElementById("searchterm").value = $("#region_input_search").select2("val");
	}
	$.ajax({url: document.getElementById("searchform").getAttribute("action"),
			type: "GET",
			data: {
				searchterm: document.getElementById("searchterm").value,
				searchtype: document.getElementById("dropdown_selection").innerHTML
			},
			success: function(result){
				console.log("success: " + result);
				clearSessions();
				loadSessions(result);
			},
			error: function(xhr, status, error){
				console.log("xhr: " + xhr.responseText);
				console.log("status: " + status);
				console.log("error: " + error);
			}
	});
}

function createStatement()
{
	console.log("create statement phase: " + document.getElementById("create_statement_phase").value);
	$.ajax({url: document.getElementById("create_statement").getAttribute("action"),
			type: "POST",
			data: {
				session_name: document.getElementById("create_statement_session").value,
				vision_statement: document.getElementById("vision_statement").value,
				phase: document.getElementById("create_statement_phase").value
			},
			success: function(result){
				document.getElementById('statement_submitted').style = 'display:block;';
				document.getElementById('statement_form').style = 'display:none;';
				console.log("success: " + result);
				document.getElementById("submitted_statement_p").innerHTML = "<b>Submitted: </b>" + document.getElementById("vision_statement").value;
			},
			error: function(xhr, status, error){
				console.log("xhr: " + xhr.responseText);
				console.log("status: " + status);
				console.log("error: " + error);
			}
	});
}

function createReport()
{
	$.ajax({url: document.getElementById("submit_report").getAttribute("action"),
			type: "POST",
			data: {
				session_name: document.getElementById("session_name").value,
				report: document.getElementById("report_textarea").value
			},
			success: function(result){
				createModalNotification("Notification", "Report submitted successfully.")
				console.log("success: " + result);
			},
			error: function(xhr, status, error){
				console.log("xhr: " + xhr.responseText);
				console.log("status: " + status);
				console.log("error: " + error);
			}
	});
}

function getStatements(phase)
{
	$.ajax({url: document.getElementById("get_statements").getAttribute("action"),
			type: "GET",
			async: false,
			data: {
				session_name: document.getElementById("session_name").value,
				phase: phase
			},
			success: function(result){
				setHtmlStatements(result);
				console.log(result);
			},
			error: function(xhr, status, error){
				console.log("xhr: " + xhr.responseText);
				console.log("status: " + status);
				console.log("error: " + error);
				results.statements = xhr;
			}
	});
}

function editStatement(phase)
{
	$.ajax({url: document.getElementById("edit_statement").getAttribute("action"),
			type: "GET",
			data: {
				session_name: document.getElementById("create_statement_session").value,
				phase: phase
			},
			success: function(result){
				document.getElementById('statement_submitted').style = 'display:none;'
				document.getElementById('statement_form').style = 'display:block;'
				document.getElementById('vision_statement').value = result;
				console.log("success: " + result);
			},
			error: function(xhr, status, error){
				console.log("xhr: " + xhr.responseText);
				console.log("status: " + status);
				console.log("error: " + error);
			}
	});
}

function getStatement(phase)
{
	$.ajax({url: document.getElementById("get_statement").getAttribute("action"),
			type: "GET",
			data: {
				session_name: document.getElementById("session_name").value,
				phase:phase,
			},
			success: function(result){
				document.getElementById("draft_vision_statement").innerHTML += result;
				console.log("success: " + result);
			},
			error: function(xhr, status, error){
				console.log("xhr: " + xhr.responseText);
				console.log("status: " + status);
				console.log("error: " + error);
			}
	});
}

function getUserCount()
{
	$.ajax({url: document.getElementById("get_usercount").getAttribute("action"),
			type: "GET",
			data: {
				session_name: document.getElementById("session_name").value
			},
			success: function(result){
				document.getElementById("usercount").innerHTML += result;
				console.log("success: " + result);
			},
			error: function(xhr, status, error){
				console.log("xhr: " + xhr.responseText);
				console.log("status: " + status);
				console.log("error: " + error);
			}
	});
}

function getChannelHistory(mphase)
{
	var phase = mphase;
	$.ajax({url: document.getElementById("get_history").getAttribute("action"),
			type: "GET",
			async: false,
			phase: phase,
			data: {
				session_name: document.getElementById("session_name").value,
			},
			success: function(result){
				loadChannelHistory(result, this.phase);
				console.log(result);
			},
			error: function(xhr, status, error){
				console.log("xhr: " + xhr.responseText);
				console.log("status: " + status);
				console.log("error: " + error);
			}
	});
}

function submitTimeData()
{
	var date_text = document.getElementById("date").value;
	var hour_text = document.getElementById("hour").value;
	var minute_text = document.getElementById("minute").value;
	$.ajax({url: document.getElementById("datetime_submit").getAttribute("action"),
			type: "POST",
			async: false,
			data: {
				session_name: document.getElementById("session_name").value,
				phase: document.getElementById("datetime_phase").value,
				date: date_text,
				hour: hour_text,
				minute: minute_text,
			},
			success: function(result){
				document.getElementById("datetime_div").style.display = "block";
				document.getElementById("form_div").style.display = "none";
				document.getElementById("datetime_text").innerHTML = "<b>"+date_text+"-"+hour_text+":"+minute_text+"</b>";
				console.log(result);
			},
			error: function(xhr, status, error){
				console.log("xhr: " + xhr.responseText);
				console.log("status: " + status);
				console.log("error: " + error);
			}
	});
}

function loadChannelHistory(result, phase)
{
	document.getElementById("message_history"+phase).innerHTML = "";
	result_json = JSON.parse(result)
	for(m in result_json.messages)
	{
		var username = "<b>" + result_json.messages[m].u.username + ": </b>";
		var message = result_json.messages[m].msg;
		console.log("message_history"+phase);
		document.getElementById("message_history"+phase).innerHTML += "<p>" + username + message + "</p>";
	}
}

function clearSessions()
{
	var visionsession_list = document.getElementById("created_visionsession_list");
	while(visionsession_list.hasChildNodes())
	{
		visionsession_list.removeChild(visionsession_list.lastChild);
	}
	visionsession_list = document.getElementById("joined_visionsession_list");
	while(visionsession_list.hasChildNodes())
	{
		visionsession_list.removeChild(visionsession_list.lastChild);
	}
	visionsession_list = document.getElementById("public_visionsession_list");
	while(visionsession_list.hasChildNodes())
	{
		visionsession_list.removeChild(visionsession_list.lastChild);
	}
}

function createSessionElement(s, json)
{
	var formobj = document.createElement("form");
		formobj.action ="visionprofile";
		formobj.method = "get";
		var hiddenInput = document.createElement("input");
		hiddenInput.type = "hidden";
		hiddenInput.name = "session_name";
		hiddenInput.value = json.session_name;
		formobj.appendChild(hiddenInput);
		var listobj = document.createElement("li");

		var sessionDiv = document.createElement("div");
		var textDiv = document.createElement("div");
		textDiv.style = "float:left; margin:5px;";
		var nameDiv = document.createElement("div");
		nameDiv.style = "margin:5px";
		nameDiv.innerHTML = "<b>" + json.session_name + "</b>"
		var descDiv = document.createElement("div");
		descDiv.style = "margin:5px";
		descDiv.innerHTML = "<i>" + json.session_description + "</i>"
		var buttonDiv = document.createElement("div");
		var button = document.createElement("button");
		button.className = "to_session_button";
		buttonDiv.className = "to_session_div";
		button.setAttribute("onclick", "this.parentNode.parentNode.nextSibling.submit()");
		button.innerHTML = "<i class='fa fa-chevron-right fa-2x' aria-hidden='true'></i>";
		buttonDiv.appendChild(button);
		buttonDiv.style = "float:right; height:60px;width:60px;";
		sessionDiv.appendChild(textDiv);
		textDiv.appendChild(nameDiv);
		textDiv.appendChild(descDiv);
		sessionDiv.appendChild(buttonDiv);

		if(s%2==0)
		{
			listobj.style = "border-bottom: 1px solid #0099CC;overflow:auto;background:#0099CC;color:white;";
			button.style = "border:none;background:none;height:60px;width:60px;color:white;";
		}
		else
		{
			listobj.style = "border-bottom: 1px solid #0099CC;overflow:auto;";
			button.style = "border:none;background:none;height:60px;width:60px;";
		}

		listobj.appendChild(sessionDiv);
		listobj.appendChild(formobj);
		return listobj;
}

function loadSessions(result) {;
	result_json = JSON.parse(result);
	var created = result_json.sessions.created;
	var joined = result_json.sessions.joined;
	var public = result_json.sessions.public;
	if(created.length == 0)
	{
		var p = document.createElement('p');
		p.innerHTML = "You have not created any Collaborative Vision Building Sessions";
		document.getElementById("created_visionsession_list").appendChild(p);
	}
	else {
        for (s in created) {
            listobj = createSessionElement(s, created[s]);
            document.getElementById("created_visionsession_list").appendChild(listobj);
        }
    }

    if(joined.length == 0)
	{
		var p = document.createElement('p');
		p.innerHTML = "You have not joined any Collaborative Vision Building Sessions";
		document.getElementById("joined_visionsession_list").appendChild(p);
	}
	else {
        for (s in joined) {
            listobj = createSessionElement(s, joined[s]);
            document.getElementById("joined_visionsession_list").appendChild(listobj);
        }
    }

    if(public.length == 0)
	{
		var p = document.createElement('p');
		p.innerHTML = "There are no public Collaborative Vision Building Sessions";
		document.getElementById("public_visionsession_list").appendChild(p);
	}
	else {
        for (s in public) {
            listobj = createSessionElement(s, public[s]);
            document.getElementById("public_visionsession_list").appendChild(listobj);
        }
    }
}

function expand()
{
	if(document.getElementById('submitted_statements').getAttribute('loaded') == 'false')
	{
		getStatements("2");
		document.getElementById('submitted_statements').setAttribute('loaded', 'true');
	}
	if(document.getElementById('expand_button').innerHTML == "expand")
	{
		document.getElementById('expand_button').innerHTML = "collapse";
	}
	else
	{
		document.getElementById('expand_button').innerHTML = "expand";
	}
}

function setHtmlStatements(statements)
{
	document.getElementById('submitted_statements').innerHTML = "";
	result_json = JSON.parse(statements);
	for(r in result_json.statements)
	{
		document.getElementById('submitted_statements').innerHTML += "<p>" + result_json.statements[r] + "</p>";
	}
}

function printPDF()
{
	document.getElementById('back_btn_container').style.display = 'none';

	try
	{
		document.getElementById('owner_dropdown').style.display = 'none';
	}
	catch(err)
	{
		console.log(err);
	}

	document.getElementById('html_string').value = "";
	var phase1 = document.getElementById('phase_1').outerHTML;

	if(document.getElementById('submitted_statements').getAttribute('loaded') == 'false')
	{
		getStatements('2');
		document.getElementById('submitted_statements').setAttribute('loaded', 'true');
	}
	$('#submitted_statements').collapse('show');
	document.getElementById('expand_button').style.display = "none";
	var phase2 = document.getElementById('phase_2_sum').outerHTML;

	var phase3 = document.getElementById('phase_3_sum').outerHTML;

	getChannelHistory('_p4');
	document.getElementById('get_history_button').style.display = "none";
	var phase4 = document.getElementById('phase_4_sum').outerHTML;

	var phase5 = document.getElementById('phase_5_sum').outerHTML;

	document.getElementById('export_pdf').style.display = "none";
	var phase6 = document.getElementById('phase_6').outerHTML;

	var printWindow = "";
	printWindow += '<html><head><title>DIV Contents</title>';
	printWindow += '</head><body >';
	printWindow += '<h1>'+ document.getElementById('session_name').value +'</h1>';
	printWindow += phase1;
	printWindow += phase2;
	printWindow += phase3;
	printWindow += phase4;
	printWindow += phase5;
	printWindow += phase6;
	printWindow += '</body></html>';

	document.getElementById('html_string').value = printWindow;

	document.getElementById('expand_button').style.display = "block";
	document.getElementById('get_history_button').style.display = "block";
	document.getElementById('export_pdf').style.display = "block";
	document.getElementById('back_btn_container').style.display = 'block';
	try
	{
		document.getElementById('owner_dropdown').style.display = 'block';
	}
	catch(err)
	{
		console.log(err);
	}

	console.log(printWindow);

	 document.getElementById('export_form').submit();
}

function exportPDF()
{
	$.ajax({url: document.getElementById("export_pdf").getAttribute("action"),
			type: "GET",
			data: {
				html_string: printPDF(),
			},
			success: function(result){
				console.log(result);
			},
			error: function(xhr, status, error){
				console.log("xhr: " + xhr.responseText);
				console.log("status: " + status);
				console.log("error: " + error);
			}
	});
}

function dropdown(dropdown) {
	$('.dropdown-content:not(#'+dropdown+'):visible').toggle();
	$('#'+dropdown).toggle();
}

function searchSelection(selection)
{
	document.getElementById("dropdown_selection").innerHTML = selection;

	if(selection == "Region")
	{
		document.getElementById("searchselect_div").style.display = "inline";
		document.getElementById("searchterm_div").style.display = "none";
	}
	else
	{
		document.getElementById("searchselect_div").style.display = "none";
		document.getElementById("searchterm_div").style.display = "block";
	}
	dropdown("myDropdown");
}

function createModalNotification(header, content)
{
	var modal = document.createElement("div");
	modal.className = "s3_modal";
	modal.id = "notification_modal";

	var headerDiv = document.createElement("div");
	headerDiv.className = "modalheader";

	var headerText = document.createElement("div");
	headerText.style = "float:left";

	var closeDiv = document.createElement("div");
	closeDiv.style = "float:right";

	var closeSpan = document.createElement("div");
	closeSpan.className = "close";
	closeSpan.innerHTML = "&times";
	closeSpan.onclick = function(){
		$("#notification_modal").remove();
	};

	var headerElem = document.createElement("p");
	headerElem.innerHTML = header;

	var contentElem = document.createElement("p");
	contentElem.innerHTML = content;

	modal.appendChild(headerDiv);
	headerDiv.appendChild(headerText);
	headerText.appendChild(headerElem);
	headerDiv.appendChild(closeDiv);
	closeDiv.appendChild(closeSpan);

	modal.appendChild(contentElem);

	document.body.appendChild(modal);
	document.getElementById("notification_modal").style.display = "block";
}

from django.views import View
import google.oauth2.credentials
import google_auth_oauthlib.flow
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import render
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.http import HttpResponse
from django.contrib.sessions.backends.db import SessionStore
class LoginByGoogle(View):
    def get(self,request):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'Home/client_secret.json',
            scopes=['https://www.googleapis.com/auth/userinfo.profile'])


        flow.redirect_uri = 'http://localhost:8000/LoginGoogleResponse'
        

        authorization_url, state = flow.authorization_url(
            
            access_type='offline',
            state='home',
             include_granted_scopes='true'
             )
        session = SessionStore()
        request.session['state'] = state
        session.save()
        
        return redirect(authorization_url)
class LoginGoogleResponse(View):
    def get(self,request):
        state = request.session.get('state','')
        
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'Home/client_secret.json',
            scopes=['https://www.googleapis.com/auth/userinfo.profile']
            ,state=state
            )

        
        flow.redirect_uri = request.build_absolute_uri(reverse('oauth2callback'))
        
        authorization_response = request.build_absolute_uri()
        print("đay la url response: ",authorization_response)
        flow.fetch_token(authorization_response=authorization_response)

        credentials = flow.credentials
        session = SessionStore()
        request.session['credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}
        print(credentials.refresh_token)
        session.save()

        return redirect(request.build_absolute_uri(reverse('home')))

class Home(View):
    def get(self,request):
        credentials_dict = request.session.get('credentials')
        print(credentials_dict)
        if not credentials_dict:
            return redirect('authorize')

        credentials = Credentials.from_authorized_user_info(info=credentials_dict)
        
        
        try:
            service = build('people', 'v1', credentials=credentials)
            print(service)
            person = service.people().get(resourceName='people/me', personFields='names').execute()
            print('day la',person)
            return render(request, 'person.html', {'person': person})
        except HttpError as error:
            return render(request, 'error.html', {'error': error})

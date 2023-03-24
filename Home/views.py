from django.shortcuts import render
from django.views import View
import google.oauth2.credentials
import google_auth_oauthlib.flow
from django.shortcuts import redirect


class LoginByGoogle(View):
    def get(self,request):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'client_secret.json',
            scopes=['https://www.googleapis.com/auth/drive.metadata.readonly'])


        flow.redirect_uri = 'https://www.example.com/oauth2callback'


        authorization_url, state = flow.authorization_url(
            
            access_type='offline',
        
            include_granted_scopes='true')
        return redirect(authorization_url)
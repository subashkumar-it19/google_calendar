from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Set up the OAuth2 flow
SCOPES = ['https://www.googleapis.com/oauth2/v1/certs']
FLOW = Flow.from_client_secrets_file(
    'secrets/client_secret.json',
    scopes=SCOPES,
    redirect_uri='http://localhost:8000/rest/v1/calendar/redirect'
)


class GoogleCalendarInitView(APIView):
    def get(self, request):
        # Generate the authorization URL
        auth_url, state = FLOW.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )

        # Save the state to the session
        request.session['state'] = state
        request.session.modified = True

        # Redirect the user to the authorization URL
        return Response({'auth_url': auth_url}, status=status.HTTP_200_OK)


class GoogleCalendarInitCallbackView(APIView):
    def get(self, request):
        # Validate the state
        state = request.session.get('state', None)
        if state is None or state != request.query_params.get('state'):
            return Response({'error': 'Invalid state'}, status=status.HTTP_400_BAD_REQUEST)

        # Exchange the authorization code for a token
        code = request.query_params.get('code')
        FLOW.fetch_token(code=code)

        # Create a service object to access the Google Calendar API
        credentials = Credentials.from_authorized_user_info(FLOW.credentials)
        service = build('calendar', 'v3', credentials=credentials)

        # Get the user's primary calendar
        calendar = service.calendars().get(calendarId='primary').execute()

        # Return the calendar information
        return Response(calendar, status=status.HTTP_200_OK)

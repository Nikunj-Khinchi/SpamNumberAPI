from rest_framework import viewsets, status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from .models import Contact, SpamReport
from .serializers import UserSerializer, ContactSerializer, SpamReportSerializer
from .utils import calculate_spam_likelihood
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class SpamReportViewSet(viewsets.ModelViewSet):
    queryset = SpamReport.objects.all()
    serializer_class = SpamReportSerializer
    permission_classes = [permissions.IsAuthenticated]

class SearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', '')
        search_by = request.query_params.get('search_by', 'name')
        if search_by == 'name':
            results = User.objects.filter(Q(name__icontains=query))
            results = sorted(results, key=lambda x: x.name.lower().startswith(query.lower()), reverse=True)
        else:
            results = User.objects.filter(Q(phone_number__icontains=query))
        
        serialized_results = []
        for result in results:
            spam_likelihood = calculate_spam_likelihood(result.phone_number)
            serialized_results.append({
                'name': result.name,
                'phone_number': result.phone_number,
                'spam_likelihood': spam_likelihood
            })
        return Response(serialized_results, status=status.HTTP_200_OK)



class FetchProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class VerifyTokenView(APIView):
    permission_classes = []

    def post(self, request):
        token = request.data.get('token')

        try:
            # Verify the token
            UntypedToken(token)

            # Decode the token to get the user ID
            user_id = UntypedToken(token).payload.get('user_id')
            user = User.objects.get(id=user_id)

            # Serialize the user data
            serializer = UserSerializer(user)

            # Return the user details
            return Response(serializer.data, status=status.HTTP_200_OK)

        except (InvalidToken, TokenError):
            return Response({"detail": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from profiles_app.models import Profile
from .serializers import (
    ProfileSerializer, 
    BusinessProfileListSerializer, 
    CustomerProfileListSerializer
)


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve and update user profile by pk.
    Anyone can view profiles, only the profile owner can modify their profile.
    """
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'
    
    def get_object(self):
        """
        Return the profile based on pk in URL.
        Raises 404 if profile doesn't exist.
        """
        pk = self.kwargs.get('pk')
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise NotFound("Das Benutzerprofil wurde nicht gefunden.")
    
    def get(self, request, *args, **kwargs):
        """
        Retrieve a user's profile.
        Returns:
            200: Die Profildaten wurden erfolgreich abgerufen.
            401: Benutzer ist nicht authentifiziert.
            404: Das Benutzerprofil wurde nicht gefunden.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {
                "message": "Die Profildaten wurden erfolgreich abgerufen.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    def patch(self, request, *args, **kwargs):
        """
        Partially update a user's profile.
        Only the profile owner can update their profile.
        Returns:
            200: Das Profil wurde erfolgreich aktualisiert.
            401: Benutzer ist nicht authentifiziert.
            403: Authentifizierter Benutzer ist nicht der Eigentümer des Profils.
            404: Das Benutzerprofil wurde nicht gefunden.
        """
        instance = self.get_object()
        
        # Check if user is the owner of this profile
        if instance.user.user != request.user:
            return Response(
                {"error": "Authentifizierter Benutzer ist nicht der Eigentümer des Profils."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Das Profil wurde erfolgreich aktualisiert.",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "error": "Validierungsfehler",
                    "details": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def put(self, request, *args, **kwargs):
        """
        Disable full update - only partial updates allowed.
        """
        return Response(
            {"detail": "Full update not allowed. Use PATCH for partial updates."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def delete(self, request, *args, **kwargs):
        """
        Disable delete - profiles cannot be deleted independently.
        """
        return Response(
            {"detail": "Profile deletion not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class BaseProfileListView(generics.ListAPIView):
    """
    Base view for profile lists - shared functionality.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Get profiles filtered by user type with optimized queries.
        """
        return Profile.objects.filter(
            user__type=self.user_type
        ).select_related('user__user')
    
    def list(self, request, *args, **kwargs):
        """
        Return list of profiles filtered by type.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        return Response(
            {
                "message": f"Profile mit Typ '{self.user_type}' erfolgreich abgerufen.",
                "count": len(serializer.data),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


class BusinessProfileListView(BaseProfileListView):
    """
    List all business profiles.
    """
    serializer_class = BusinessProfileListSerializer
    user_type = 'business'


class CustomerProfileListView(BaseProfileListView):
    """
    List all customer profiles.
    """
    serializer_class = CustomerProfileListSerializer
    user_type = 'customer'


#TODO: MUSS noch durchgeschaut werden und getestet 
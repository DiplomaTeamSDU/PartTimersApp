from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class TokenPairSerializer(TokenObtainPairSerializer):
    """
    Serializer for obtaining a JSON web token pair.

    This serializer returns a JSON response that contains both the access and
    refresh tokens in the following format:

    {
        "access": "<access_token>",
        "refresh": "<refresh_token>"
    }
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data

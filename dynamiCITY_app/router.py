from rest_framework import routers

class ApiDocumentationView(routers.APIRootView):
    """
    This is the homepage for available api routes. For more information see the project's documentation.    
    """
    pass


class DocumentedRouter(routers.DefaultRouter):
    APIRootView = ApiDocumentationView

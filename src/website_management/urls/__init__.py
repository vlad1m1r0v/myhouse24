from .website_management import urlpatterns as management_urls
from .website import urlpatterns as website_urls

urlpatterns = [*management_urls, *website_urls]
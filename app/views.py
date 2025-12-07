from django.http import HttpResponse, HttpRequest


def home(_request: HttpRequest) -> HttpResponse:
    """
    Handle requests to the home page
    """
    return HttpResponse("Hello world!")

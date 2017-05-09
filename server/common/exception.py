#!/usr/bin/python
#coding=UTF-8

"""ArchRest exception subclasses"""
import urlparse


class RedirectException(Exception):
    def __init__(self, url):
        self.url = urlparse.urlparse(url)


class ArchRestException(Exception):
    """
    Base ArchRest Exception

    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.
    """
    message = ("An unknown exception occurred")

    def __init__(self, message=None, *args, **kwargs):
        if not message:
            message = self.message
        try:
            message = message % kwargs
            self.message = message
        except Exception:
            # at least get the core message out if something happened
            pass
        super(ArchRestException, self).__init__(message)


class MissingArgumentError(ArchRestException):
    message = ("Missing required argument.")


class AuthBadRequest(ArchRestException):
    message = ("Connect error/bad request to Auth service at URL %(url)s.")


class Forbidden(ArchRestException):
    message = ("You are not authorized to complete this action.")


class Invalid(ArchRestException):
    message = ("Data supplied was not valid.")


class ServerError(ArchRestException):
    message = ("The request returned 500 Internal Server Error.")


class ServiceUnavailable(ArchRestException):
    message = ("The request returned 503 Service Unavilable. This "
                "generally occurs on service overload or other transient "
                "outage.")

    def __init__(self, *args, **kwargs):
        self.retry_after = (int(kwargs['retry']) if kwargs.get('retry')
                            else None)
        super(ServiceUnavailable, self).__init__(*args, **kwargs)


class Unimplementation(ServiceUnavailable):
    message = ("The method NOT implements yet.")


class UnexpectedStatus(ArchRestException):
    message = ("The request returned an unexpected status: %(status)s."
                "\n\nThe response body:\n%(body)s")


class ClientConnectionError(ArchRestException):
    message = ("There was an error connecting to a server")


class NotFound(ArchRestException):
    message = ("Resource could not be found.")
    code = 404


class NotAuthorized(ArchRestException):
    message = ("Not authorized.")
    code = 403

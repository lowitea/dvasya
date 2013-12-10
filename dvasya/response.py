# coding: utf-8

# $Id: $
from wsgiref.handlers import format_date_time
from aiohttp.protocol import HttpMessage
from aiohttp.server import RESPONSES
from dvasya.conf import settings


class HttpResponse(HttpMessage):
    status_code = 200

    HOP_HEADERS = {
        'CONNECTION',
        'KEEP-ALIVE',
        'PROXY-AUTHENTICATE',
        'PROXY-AUTHORIZATION',
        'TE',
        'TRAILERS',
        'TRANSFER-ENCODING',
        'UPGRADE',
        'SERVER',
        'DATE',
    }

    def __init__(self, content='', status=None, content_type="text/html",
                 transport=None, http_version=(1, 1), close=False):
        super().__init__(transport, http_version, close)
        self.status = status or self.status_code
        self.content = content
        self.content_type = content_type

    def attach_transport(self, transport, request):
        self.transport = transport

        self.add_header('Transfer-Encoding', 'chunked')
        accept_encoding = request.headers.get('accept-encoging', '').lower()
        if 'deflate' in accept_encoding:
            self.add_header('Content-Encoding', 'deflate')
            self.add_compression_filter('deflate')
        elif 'gzip' in accept_encoding:
            self.add_header('Content-Encoding', 'gzip')
            self.add_compression_filter('gzip')
        self.add_chunking_filter(1025)
        self.add_header("Content-Type", self.content_type)
        self.send_headers()

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value
        self.status_line = 'HTTP/{}.{} {} {}\r\n'.format(
            self.version[0], self.version[1], self.__status,
            RESPONSES.get(self.__status, (self.__status,))[0])

    def _add_default_headers(self):
        super()._add_default_headers()
        self.headers.extend((('DATE', format_date_time(None)),
                             ('SERVER', self.SERVER_SOFTWARE),))


class HttpResponseNotAllowed(HttpResponse):
    status_code = 405

    def __init__(self, permitted_methods):
        super(HttpResponseNotAllowed, self).__init__()
        self.add_header('Allow', ', '.join(permitted_methods))


class HttpResponseNotFound(HttpResponse):
    status_code = 404

    def __init__(self, no_match_error=None):
        if not settings.DEBUG:
            content = ''
        elif no_match_error:
            content = ("<h2>No match for path</h2>"
                      "<h4>{}</h4>"
                      "<h3>URLConf</h3>".format(no_match_error.args[0]))
            content += '<br/>'.join(str(p) for p in no_match_error.args[1])
        else:
            content = "<h2>Not found</h2>"
        super(HttpResponseNotFound, self).__init__(content)
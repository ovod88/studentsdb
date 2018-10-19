from datetime import datetime
from html.parser import HTMLParser
from django.http import HttpResponse


class MyHTMLParser(HTMLParser):

    def __init__(self, tag_to_append=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag_to_append = tag_to_append
        self._out = []


    def _attrstring(self, attrs):
        attrs = ['{0}="{1}"'.format(attr, val) for attr, val in attrs]
        return " ".join(attrs)

    def handle_starttag(self, tag, attrs):
        self._out.append("<{0} {1}>".format(tag, self._attrstring(attrs)))

    def handle_endtag(self, tag):
        if tag == 'body' and self.tag_to_append:
            self._out.append(self.tag_to_append)
            
        self._out.append("</{0}>".format(tag))

    def handle_data(self, data):
        data = data.replace('\\n', '\n')
        self._out.append(data)

    @property
    def cleaned_content(self):
        return "".join(self._out)


class RequestTimeMiddleware:

    def __init__(self, get_response=None):
        self.get_response = get_response


    def __call__(self, request):
        response = self.process_request(request)
        if response is None:
            response = self.get_response(request)

        response = self.process_response(request, response)

        return response

    def process_request(self, request):
        request.start_time = datetime.now()
        return None

    def process_response(self, request, response):
        if not hasattr(request, 'start_time'):
            return response

        request.end_time = datetime.now()
        diff_tag = '<br />Request took: %s' % str(request.end_time - request.start_time)

        if 'text/html' in response.get('Content-Type', ''):
            parser = MyHTMLParser(diff_tag)
            parser.feed(response.content.decode("utf-8"))

            response.content = parser.cleaned_content.encode()

        return response

    def process_view(self, request, view, args, kwargs):
        return None

    def process_template_response(self, request, response):
        return response

    def process_exception(self, request, exception):
        return HttpResponse('Exception found: %s' % exception)

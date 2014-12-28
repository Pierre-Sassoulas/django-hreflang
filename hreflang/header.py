
"""
	Add hreflang response headers as specified by Google

	https://support.google.com/webmasters/answer/189077?hl=en
"""

from django.core.urlresolvers import resolve
from django.utils.translation import get_language
from hreflang import language_codes, reverse


def hreflang_headers(response, request = None, path = None):
	"""
		Adds hreflang headers to a HttpResponse object

		:param response: the HttpResponse to add headers to
		:param path: the current path for which to add alternate language versions
		:param request: the request, which is used to find path (ignored if path is set directly)
		:return: response is modified and returned
	"""
	assert request or path, 'hreflang_headers needs the current url, please either provide request or a path'
	reverse_match = resolve(path or request.path)
	links = []
	for lang in language_codes():
		new_url = reverse(reverse_match.view_name, lang = lang, kwargs = reverse_match.kwargs)
		links.append('<{1}>; rel="alternate"; hreflang="{0}"'.format(lang, new_url))
	print(response['Link'])
	response['Link'] = '{0},'.format(response['Link']) if response['Link'] else ''
	response['Link'] += ','.join(links)
	return response
	#'Link: <http://es.example.com/>; rel="alternate"; hreflang="es"'


class AddHreflangToResponse():
	"""
		A middleware that applies hreflang_headers to all responses (adding hreflang headers).
	"""
	def process_response(request, response):
		return hreflang_headers(response, request = request)



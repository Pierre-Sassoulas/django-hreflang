
"""
	Create hreflang tags as specified by Google

	https://support.google.com/webmasters/answer/189077?hl=en
"""

from django import template
from django.core.urlresolvers import resolve
from hreflang import reverse, language_codes
from django.utils.translation import get_language
from hreflang.functions import languages


register = template.Library()


@register.simple_tag(takes_context = True)
def translate_url(context, lang):
	"""
		Translate an url to a specific language.
	"""
	assert 'request' in context, 'translate_url needs request context'
	reverse_match = resolve(context['request'].path)
	return reverse(reverse_match.view_name, lang = lang, kwargs = reverse_match.kwargs)


@register.simple_tag(takes_context = True)
def hreflang_tags(context):
	"""
		Create all hreflang <link> tags (which includes the current document as per the standard).
	"""
	assert 'request' in context, 'hreflang_tags needs request context'
	hreflang_html = ''
	reverse_match = resolve(context['request'].path)
	for lang in language_codes():
		new_url = reverse(reverse_match.view_name, lang = lang, use_lang_prefix = False, kwargs = reverse_match.kwargs)
		hreflang_html += '<link rel="alternate" hreflang="{0}" href="{1}" />\n'.format(lang, new_url)
	return hreflang_html


@register.simple_tag(takes_context = True)
def lang_list(context):
	"""
		HTML list items with links to each language version of this document. The current document is included without link and with a special .hreflang_current_language class.
	"""
	assert 'request' in context, 'lang_list needs request context'
	hreflang_html = ''
	reverse_match = resolve(context['request'].path)
	for lang_code, lang_name in languages():
		new_url = reverse(reverse_match.view_name, lang = lang_code, kwargs = reverse_match.kwargs)
		if lang_code == get_language():
			hreflang_html += '<li class="hreflang_current_language"><strong>{0}</strong></li>\n'.format(lang_name)
		else:
			hreflang_html += '<li><a href="{0}" >{1}</a></li>\n'.format(new_url, lang_name)
	return hreflang_html


@register.simple_tag(takes_context = True)
def other_lang_list(context):
	"""
		Like lang_list, but the current language is excluded.
	"""
	assert 'request' in context, 'other_lang_list needs request context'
	hreflang_html = ''
	reverse_match = resolve(context['request'].path)
	for lang_code, lang_name in languages():
		if lang_code == get_language(): continue
		new_url = reverse(reverse_match.view_name, lang = lang_code, kwargs = reverse_match.kwargs)
		hreflang_html += '<li><a href="{0}" >{1}</a></li>\n'.format(new_url, lang_name)
	return hreflang_html



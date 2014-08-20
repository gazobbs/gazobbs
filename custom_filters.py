import datetime
from google.appengine.ext import webapp


register = webapp.template.create_template_register()


def jshift(body):
	return body + datetime.timedelta(hours=9)
register.filter(jshift)

#!/usr/bin/env python
import urlparse
import traceback


# Strip the proxy hostname part of the passed URL
def rewrite_URL_strip(url, config):
	try:
		res = urlparse.urlsplit(url)

		if res[1]:
			newres = [ item for item in res ]
			host = res[1].split(":")[0]
			if host.endswith(config.hostname):
				host = host.split(config.hostname)[0]
			newres[1] = host

			url = urlparse.urlunsplit(newres)
	except Exception, e:
		pass
	return url

# Rewrite the URL and add the proxy's HTTP or HTTPS ports when necessary.
# For absolute URLs without scheme, use the same scheme as used to access
# the proxy (using the 'ssl' flag)
def rewrite_URL(url, config, ssl):
	try: 
		# Strip our own hostname for the rewrites to work
		url = rewrite_URL_strip(url,config)
		res = urlparse.urlsplit(url) 
		need_rewrite = False

		# Handle rewrites
		for (f, t) in config.rewrites:
			if res[1] and res[1].split(":")[0].lower() == f.lower() and (res[0] == '' or res[0] == 'http' or res[0] == 'https'): 
				newres = [ item for item in res ]
				host = t

				# No scheme, use the scheme used to access proxy
				if res[0] == '': # res[0] == scheme
					if ssl:
						newres[0]='https'
					else:
						newres[0]='http'
		
				# Add port of proxy
				if newres[0] == 'http':
					port = config.http_port
				elif newres[0] == 'https':
					port = config.https_port

				newres[1] = host + ":" + str(port)
				url = urlparse.urlunsplit(newres) 
				return url

		# Handle absolute HTTP or HTTPS URL
		if res[1] and (res[0] == '' or res[0] == 'http' or res[0] == 'https'): 
			newres = [ item for item in res ] 
			host = res[1].split(":")[0]

			# No scheme, use the scheme used to access proxy
			if res[0] == '': # res[0] == scheme
				if ssl:
					newres[0]='https'
				else:
					newres[0]='http'
	
			# Add port of proxy
			if newres[0] == 'http':
				port = config.http_port
			elif newres[0] == 'https':
				port = config.https_port

			newres[1] = host + "." + config.hostname + ":" + str(port)
			url = urlparse.urlunsplit(newres) 
	except Exception, e: 
		pass
	
	return url

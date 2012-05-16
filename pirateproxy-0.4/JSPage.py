import re
import Util

# Class used to parse and rewrite JS files and snippets
class JSPage:
	BLKSIZE=4096

	def __init__(self, config, ssl, reader, writer):
		self.config = config
		self.ssl = ssl
		self.reader = reader
		self.writer = writer
		self.input_buffer = ''
		self.output_buffer = ''
		self.pos = 0
		self.delimiter = ''
		self.url_regex = re.compile("^https?:\\\\?/\\\\?/", re.I)
		self.url_char_regex = re.compile("[a-zA-Z0-9\-\.]")
		self.tlds = {"AC":True,"AD":True,"AE":True,"AERO":True,"AF":True,"AG":True,"AI":True,"AL":True,"AM":True,"AN":True,"AO":True,"AQ":True,"AR":True,"ARPA":True,"AS":True,"ASIA":True,"AT":True,"AU":True,"AW":True,"AX":True,"AZ":True,"BA":True,"BB":True,"BD":True,"BE":True,"BF":True,"BG":True,"BH":True,"BI":True,"BIZ":True,"BJ":True,"BM":True,"BN":True,"BO":True,"BR":True,"BS":True,"BT":True,"BV":True,"BW":True,"BY":True,"BZ":True,"CA":True,"CAT":True,"CC":True,"CD":True,"CF":True,"CG":True,"CH":True,"CI":True,"CK":True,"CL":True,"CM":True,"CN":True,"CO":True,"COM":True,"COOP":True,"CR":True,"CU":True,"CV":True,"CW":True,"CX":True,"CY":True,"CZ":True,"DE":True,"DJ":True,"DK":True,"DM":True,"DO":True,"DZ":True,"EC":True,"EDU":True,"EE":True,"EG":True,"ER":True,"ES":True,"ET":True,"EU":True,"FI":True,"FJ":True,"FK":True,"FM":True,"FO":True,"FR":True,"GA":True,"GB":True,"GD":True,"GE":True,"GF":True,"GG":True,"GH":True,"GI":True,"GL":True,"GM":True,"GN":True,"GOV":True,"GP":True,"GQ":True,"GR":True,"GS":True,"GT":True,"GU":True,"GW":True,"GY":True,"HK":True,"HM":True,"HN":True,"HR":True,"HT":True,"HU":True,"ID":True,"IE":True,"IL":True,"IM":True,"IN":True,"INFO":True,"INT":True,"IO":True,"IQ":True,"IR":True,"IS":True,"IT":True,"JE":True,"JM":True,"JO":True,"JOBS":True,"JP":True,"KE":True,"KG":True,"KH":True,"KI":True,"KM":True,"KN":True,"KP":True,"KR":True,"KW":True,"KY":True,"KZ":True,"LA":True,"LB":True,"LC":True,"LI":True,"LK":True,"LR":True,"LS":True,"LT":True,"LU":True,"LV":True,"LY":True,"MA":True,"MC":True,"MD":True,"ME":True,"MG":True,"MH":True,"MIL":True,"MK":True,"ML":True,"MM":True,"MN":True,"MO":True,"MOBI":True,"MP":True,"MQ":True,"MR":True,"MS":True,"MT":True,"MU":True,"MUSEUM":True,"MV":True,"MW":True,"MX":True,"MY":True,"MZ":True,"NA":True,"NAME":True,"NC":True,"NE":True,"NET":True,"NF":True,"NG":True,"NI":True,"NL":True,"NO":True,"NP":True,"NR":True,"NU":True,"NZ":True,"OM":True,"ORG":True,"PA":True,"PE":True,"PF":True,"PG":True,"PH":True,"PK":True,"PL":True,"PM":True,"PN":True,"PR":True,"PRO":True,"PS":True,"PT":True,"PW":True,"PY":True,"QA":True,"RE":True,"RO":True,"RS":True,"RU":True,"RW":True,"SA":True,"SB":True,"SC":True,"SD":True,"SE":True,"SG":True,"SH":True,"SI":True,"SJ":True,"SK":True,"SL":True,"SM":True,"SN":True,"SO":True,"SR":True,"ST":True,"SU":True,"SV":True,"SX":True,"SY":True,"SZ":True,"TC":True,"TD":True,"TEL":True,"TF":True,"TG":True,"TH":True,"TJ":True,"TK":True,"TL":True,"TM":True,"TN":True,"TO":True,"TP":True,"TR":True,"TRAVEL":True,"TT":True,"TV":True,"TW":True,"TZ":True,"UA":True,"UG":True,"UK":True,"US":True,"UY":True,"UZ":True,"VA":True,"VC":True,"VE":True,"VG":True,"VI":True,"VN":True,"VU":True,"WF":True,"WS":True,"XN--0ZWM56D":True,"XN--11B5BS3A9AJ6G":True,"XN--3E0B707E":True,"XN--45BRJ9C":True,"XN--80AKHBYKNJ4F":True,"XN--80AO21A":True,"XN--90A3AC":True,"XN--9T4B11YI5A":True,"XN--CLCHC0EA0B2G2A9GCD":True,"XN--DEBA0AD":True,"XN--FIQS8S":True,"XN--FIQZ9S":True,"XN--FPCRJ9C3D":True,"XN--FZC2C9E2C":True,"XN--G6W251D":True,"XN--GECRJ9C":True,"XN--H2BRJ9C":True,"XN--HGBK6AJ7F53BBA":True,"XN--HLCJ6AYA9ESC7A":True,"XN--J6W193G":True,"XN--JXALPDLP":True,"XN--KGBECHTV":True,"XN--KPRW13D":True,"XN--KPRY57D":True,"XN--LGBBAT1AD8J":True,"XN--MGBAAM7A8H":True,"XN--MGBAYH7GPA":True,"XN--MGBBH1A71E":True,"XN--MGBC0A9AZCG":True,"XN--MGBERP4A5D4AR":True,"XN--O3CW4H":True,"XN--OGBPF8FL":True,"XN--P1AI":True,"XN--PGBS0DH":True,"XN--S9BRJ9C":True,"XN--WGBH1C":True,"XN--WGBL6A":True,"XN--XKC2AL3HYE2A":True,"XN--XKC2DL3A5EE0H":True,"XN--YFRO4I67O":True,"XN--YGBI2AMMX":True,"XN--ZCKZAH":True,"XXX":True,"YE":True,"YT":True,"ZA":True,"ZM":True,"ZW":True}
#"

	def really_rewrite_part(self, s, start_pos, end_pos, add_port):
		if start_pos == end_pos:
			return s
	
		if s.lower().endswith(self.config.hostname):
			return s

		if self.ssl:
			port = self.config.https_port
		else:
			port = self.config.http_port

		# Not necessary to use standard port numbers. Assume proxy is not
		# doing HTTP on 443 or HTTPS on 80
		if port == 80 or port == 443:
			portstr = ''
		else:
			portstr = ':' + str(port)

		# Cut out port number if it's there and replace with own
		# port
		if end_pos < len(s) and s[end_pos] == ':':
			new_end_pos = end_pos + 1
			while new_end_pos < len(s) and s[new_end_pos] >= '0' and s[new_end_pos] <= '9':
				new_end_pos += 1 

			if new_end_pos == end_pos + 1:
				return s

			return "".join([s[:start_pos] + s[start_pos:end_pos], ".", self.config.hostname, portstr, s[new_end_pos:]]) 
		else:
			if not add_port:
				portstr = ''

			return "".join([s[:start_pos], s[start_pos:end_pos], ".", self.config.hostname, portstr, s[end_pos:]])



	# Determine if a part is a domain name or URL and rewrite it
	def rewrite_part(self, s):
		news = s

		if re.match(self.url_regex,s):
			start_pos = s.find('/', s.find('/')+1)+1
			end_pos = start_pos
			while end_pos < len(s) and re.match(self.url_char_regex, s[end_pos]):
				end_pos += 1

			if not s[start_pos:end_pos].lower().endswith(self.config.hostname):
				news = self.really_rewrite_part(s, start_pos, end_pos, True)
				
			return news

		# Not a URL, but may be a hostname
		start_pos=0
		end_pos=0
		while end_pos < len(s) and re.match(self.url_char_regex, s[end_pos]):
			end_pos += 1

		dot_pos=s.rfind(".", start_pos, end_pos) 
		if dot_pos != -1:
			tld = s[dot_pos+1:end_pos]
			if self.tlds.get(tld.upper()) and not s[start_pos:end_pos].lower().endswith(self.config.hostname):
				news=self.really_rewrite_part(s, start_pos, end_pos, False)

		return news

	# This function is used in two cases:
	# - To read data up until the first delimiter, setting the position
	#   to the first character after the delimiter and writing uninteresting
	#   data to the client
	# - To read data up until the closing delimiter, the escaped opening
	#   delimiter or even the other delimiter, keeping the data in the
	#   input buffer.
	def read_until_delimiter(self, is_closing):
		if not is_closing:
			self.delimiter = ''
		length = len(self.input_buffer)
		while length < self.config.max_page_size:
			# If there's data in the input buffer, try to find a delimiter there
			# first
			if self.pos < len(self.input_buffer):
				for pos in range(self.pos, len(self.input_buffer)):
					if self.input_buffer[pos] == '"' or self.input_buffer[pos] == "'":
						# Keep the data in the input buffer when searching
						# for closing delimiter
						if is_closing:
							self.pos = pos
							pass
						else:
							pos += 1
							self.delimiter = self.input_buffer[pos-1]
							self.output_buffer += self.input_buffer[:pos]
							self.input_buffer = self.input_buffer[pos:]
							self.pos = 0
							self.write_output(False)
						return

			# If there was no data in the input buffer or no delimiter was
			# found yet, keep on reading

			# First, empty the possible still filled input buffer if nothing
			# interesting was found and we are searching for the opening
			# delimiter
			if not is_closing:
				self.output_buffer += self.input_buffer
				self.input_buffer = ''
				self.pos = 0
				length = 0
				self.write_output(False)

			s = self.reader(self.BLKSIZE)
			if not s or len(s) == 0:
				self.pos =  -1
				return

			self.input_buffer += s
			length += len(s)

	# Returns True if a delimiter is escaped, false if it is not
	def escaped(self, pos):
		escape = False

		for i in range(pos-1, 0, -1):
			if self.input_buffer[pos] == '\\':
				escape ^= escape
			else:
				return escape
		return escape

	# Rewrite the JS page/snippet by finding string 'parts': pieces of text
	# delimited by a single or double quote character. Such parts may contain
	# subparts, delimited by the 'other' quoting character, or using escapes.
	def rewrite(self):
		while True:
			self.read_until_delimiter(False)

			# No delimiter found (anymore), return
			if self.pos == -1:
				self.output_buffer += self.input_buffer
				self.write_output(True)
				return

			begin_pos = self.pos
			self.read_until_delimiter(True)

			# Is this delimiter is non-escaped and equal to the opening
			# delimiter or the closing delimiter was not found and the page is
			# too large, then rewrite it as a possible URL and continue the 
			# main loop
			if self.delimiter == self.input_buffer[self.pos] and not self.escaped(self.pos) or self.delimiter not in ['"', "'"]:
				self.output_buffer += self.rewrite_part(self.input_buffer[:self.pos]) + self.input_buffer[self.pos]
				self.input_buffer = self.input_buffer[self.pos+1:]
				self.pos = 0
				self.write_output(False)
				continue

			# This delimiter contains sub-parts, starting at the current 
			# position. Write any data before this sub-part to the client and
			# read until the end of the sub-part or the end of the main-part
			begin_delim = self.input_buffer[self.pos]
			self.output_buffer += self.input_buffer[:self.pos+1]
			self.input_buffer = self.input_buffer[self.pos+1:]
			self.pos = 0
			self.write_output(False)
			while True:
				self.read_until_delimiter(True)

				if self.pos == -1:
					# No data found anymore, write any lingering data and return
					self.output_buffer += self.input_buffer
					self.input_buffer = ''
					self.pos = 0
					self.write_output(True)
					return

				if (self.input_buffer[self.pos] == self.delimiter and not self.escaped(self.pos)) or self.delimiter not in ['"', "'"]:
					# Main part delimiter reached or page too large
					self.output_buffer += self.rewrite_part(self.input_buffer[:self.pos]) + self.input_buffer[self.pos]
					self.input_buffer = self.input_buffer[self.pos+1:] 	
					self.pos = 0
					self.write_output(False)
				elif self.input_buffer[self.pos] == begin_delim or (self.input_buffer[self.pos] == self.delimiter and self.escaped(self.pos)) or self.delimiter not in ['"', "'"]:
					# Sub-part delimiter reached or page too large
					self.rewrite_part(self.input_buffer[:self.pos])
					self.output_buffer += self.rewrite_part(self.input_buffer[:self.pos]) + self.input_buffer[self.pos]
					self.input_buffer = self.input_buffer[self.pos+1:]
					self.pos = 0
					self.write_output(False)

				# Neither the main part end delimiter nor the sub-part end
				# delimiter were found. Continue.


	def write_output(self, final):
			length = len(self.output_buffer)
			for beg in range(0, length, self.BLKSIZE):
					end = beg + self.BLKSIZE
					if end > length:
						if not final:
							self.output_buffer = self.output_buffer[beg:]
							return
						end = length
					self.writer(self.output_buffer[beg:end])

			self.output_buffer = ''


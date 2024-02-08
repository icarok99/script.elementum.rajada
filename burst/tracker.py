import time
import hashlib
import socket
import random
from struct import error, pack, unpack
from kodi_six import xbmcgui
from elementum.provider import log
from future.utils import PY3
if PY3:
	from urllib.parse import urlparse, quote
else:
	from urlparse import urlparse
	from urllib import quote

# ref: https://github.com/ngosang/trackerslist

TR_OPENBT1 = ('tracker.openbittorrent.com', 80)
TR_OPENBT1_URL = 'http://tracker.openbittorrent.com:80/announce'

TR_OPENBT2 = ('tracker.openbittorrent.com', 6969)
TR_OPENBT2_URL = 'udp://tracker.openbittorrent.com:6969/announce'

TR_OPENTR = ('tracker.opentrackr.org', 1337)
TR_OPENTR_URL = 'udp://tracker.opentrackr.org:1337/announce'

TR_I2P = ('opentracker.i2p.rocks', 6969)
TR_I2P_URL = 'udp://opentracker.i2p.rocks:6969/announce'

TR_OPENDEMONII = ('open.demonii.com', 1337)
TR_OPENDEMONII_URL = 'udp://open.demonii.com:1337/announce'

TR_STEALTH = ('open.stealth.si', 80)
TR_STEALTH_URL = 'udp://open.stealth.si:80/announce'

TR_EXPLODIE = ('explodie.org', 6969)
TR_EXPLODIE_URL = 'udp://explodie.org:6969'

TR_AUCTOR = ('tracker.auctor.tv', 6969)
TR_AUCTOR_URL = 'udp://tracker.auctor.tv:6969/announce'

TR_EU = ('tracker.torrent.eu.org', 451)
TR_EU_URL = 'udp://tracker.torrent.eu.org:451/announce'

TR_PUBLICBT_URL = 'udp://tracker.publicbt.com:80' # error at checking

TR_ISTOLE_URL = 'udp://tracker.istole.it:6969' # error at checking

TR_TIMEOUT = 0.3

TR_AND = '&tr='
TR_FULL_STR =   quote(TR_AND + TR_OPENBT1_URL
					+ TR_AND + TR_OPENBT2_URL
					+ TR_AND + TR_OPENTR_URL
					+ TR_AND + TR_I2P_URL
					+ TR_AND + TR_OPENDEMONII_URL
					+ TR_AND + TR_STEALTH_URL
					+ TR_AND + TR_EXPLODIE_URL
					+ TR_AND + TR_AUCTOR_URL
					+ TR_AND + TR_EU_URL
					+ TR_AND + TR_PUBLICBT_URL
					+ TR_AND + TR_ISTOLE_URL)

class UdpTrackerAnnounceOutput:
    def __init__(self):
        self.action = None
        self.transaction_id = None
        self.interval = None
        self.leechers = None
        self.seeders = None
        self.list_sock_addr = []

    def from_bytes(self, payload):
        self.action, = unpack('>I', payload[:4])
        self.transaction_id, = unpack('>I', payload[4:8])
        self.interval, = unpack('>I', payload[8:12])
        self.leechers, = unpack('>I', payload[12:16])
        self.seeders, = unpack('>I', payload[16:20])
        self.list_sock_addr = self._parse_sock_addr(payload[20:])

    def _parse_sock_addr(self, raw_bytes):
        socks_addr = []
        # socket address : <IP(4 bytes)><Port(2 bytes)>
        # len(socket addr) == 6 bytes
        for i in range(int(len(raw_bytes) / 6)):
            start = i * 6
            end = start + 6
            ip = socket.inet_ntoa(raw_bytes[start:(end - 2)])
            raw_port = raw_bytes[(end - 2):end]
            port = raw_port[1] + raw_port[0] * 256
            socks_addr.append((ip, port))
        return socks_addr

class UdpTrackerConnection():
    def __init__(self):
        self.conn_id = pack('>Q', 0x41727101980)
        self.action = pack('>I', 0)
        self.trans_id = pack('>I', random.randint(0, 100000))

    def to_bytes(self):
        return self.conn_id + self.action + self.trans_id
        
    def from_bytes(self, payload):
        try:
            self.action, = unpack('>I', payload[:4])
            self.trans_id, = unpack('>I', payload[4:8])
            self.conn_id, = unpack('>Q', payload[8:])
        except Exception as e:
            log.debug('RAJADA_TRACKER - UdpTrackerConnection from_bytes() failed - %s' % e.__str__())

def _read_from_socket(sock):
    data = b''
    while True:
        try:
            buff = sock.recv(4096)
            #log.debug("got some response %s" % buff)
            if len(buff) <= 0:
                break
            data += buff
        except socket.error as e:
            #log.debug(e)
            break
        except Exception as e:
            log.debug("RAJADA_TRACKER - _read_from_socket failed - %s" % e.__str__())
            break
    return data

class UdpTrackerAnnounce():

    def __init__(self, info_hash, conn_id, peer_id):
        #super(UdpTrackerAnnounce, self).__init__() # error at python 2
        self.peer_id = peer_id
        self.conn_id = conn_id
        self.info_hash = info_hash
        self.trans_id = pack('>I', random.randint(0, 100000))
        self.action = pack('>I', 1)

    def to_bytes(self):
        conn_id = pack('>Q', self.conn_id)
        action = self.action
        trans_id = self.trans_id
        downloaded = pack('>Q', 0)
        left = pack('>Q', 0)
        uploaded = pack('>Q', 0)

        event = pack('>I', 0)
        ip = pack('>I', 0)
        key = pack('>I', 0)
        num_want = pack('>i', -1)
        port = pack('>h', 8000)

        msg = (conn_id + action + trans_id + self.info_hash + self.peer_id + downloaded +
               left + uploaded + event + ip + key + num_want + port)

        return msg

def get_torrent_info(torrent_obj):

	hash = torrent_obj['info_hash']
	name = torrent_obj['name']

	try:
		new_hash = bytearray.fromhex(hash) # hex bytes array from hash string
	except ValueError:
		return (hash, -1, -1)

	#id = hashlib.sha1(str(65000).encode('utf-8')).digest() # peer id
	id = hashlib.sha1(str(time.time()).encode('utf-8')).digest() # peer id

	results = []
	#results.append(get_info_from_tracker(new_hash, id, TR_OPENBT1[0], TR_OPENBT1[1])) 			# 06.02.24 not working
	#results.append(get_info_from_tracker(new_hash, id, TR_OPENBT2[0], TR_OPENBT2[1])) 			# 06.02.24 not working
	results.append(get_info_from_tracker(new_hash, id, TR_OPENTR[0], TR_OPENTR[1])) 			# 06.02.24 working
	results.append(get_info_from_tracker(new_hash, id, TR_I2P[0], TR_I2P[1])) 					# 06.02.24 working
	#results.append(get_info_from_tracker(new_hash, id, TR_STEALTH[0], TR_STEALTH[1])) 			# 06.02.24 working
	#results.append(get_info_from_tracker(new_hash, id, TR_EXPLODIE[0], TR_EXPLODIE[1])) 		# 06.02.24 working
	results.append(get_info_from_tracker(new_hash, id, TR_AUCTOR[0], TR_AUCTOR[1])) 			# 06.02.24 working
	#results.append(get_info_from_tracker(new_hash, id, TR_OPENDEMONII[0], TR_OPENDEMONII[1])) 	# 06.02.24 working

	s_array = [x[0] for x in results if x is not None]
	num_s = max(s_array) if len(s_array) > 0 else -1

	p_array = [x[1] for x in results if x is not None]
	num_p = max(p_array) if len(p_array) > 0 else -1

	#if num_s is None: num_s = -1
	#if num_p is None: num_p = -1

	log.debug('RAJADA_TRACKER - numbers for %s %s Seeders: %s Peers: %s' % (name, hash, s_array, p_array))

	return (hash, num_s, num_p)

def get_info_from_tracker(hash, peer_id, ip, port):

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.settimeout(TR_TIMEOUT)
	#sock.setblocking(0) # non blocking, wont receive correctly

	tracker_connection_input = UdpTrackerConnection()
	message = tracker_connection_input.to_bytes()
	try:
		sock.sendto(message, (ip, port))
	except Exception as e:
		#xbmcgui.Dialog().ok('Rajada Tracker', 'sock.sendto fail\n%s %s\n%s' % (ip, port, repr(e)))
		#log.debug("[COLOR blue]RAJADA_TRACKER - sock.sendto fail : %s[/COLOR]" % e.__str__())
		return None

	try:
		response = _read_from_socket(sock)
	except socket.timeout as e:
		#xbmcgui.Dialog().ok('Rajada Tracker', 'timeout fail\n%s %s\n%s' % (ip, port, repr(e)))
		#log.debug("RAJADA_TRACKER - Timeout : %s" % e.__str__())
		return None
	except Exception as e:
		#xbmcgui.Dialog().ok('Rajada Tracker', 'read fail\n%s %s\n%s' % (ip, port, repr(e)))
		#log.debug("RAJADA_TRACKER - Unexpected error when sending message : %s" % e.__str__())
		return None

	intg = list(response)
	res = UdpTrackerConnection()
	res.from_bytes(response)

	if True: #res.action == 0:
		trans_id = res.trans_id
		#conn_id = res.conn_id
		conn_id = res.conn_id if res.action == 0 else int(time.time()) # send announce apart from handshake action response

		try:
			tracker_announce_input = UdpTrackerAnnounce(hash, conn_id, peer_id)
			sock.sendto(tracker_announce_input.to_bytes(), (ip, port))
			response = _read_from_socket(sock)
		except Exception as e:
			#xbmcgui.Dialog().ok('Rajada Tracker', 'announce fail\n%s %s\n%s' % (ip, port, repr(e)))
			#log.debug('RAJADA_TRACKER - announce failed for %s %s - %s' % (ip,port,e.__str__()))
			return None

		if not response:
			#log.debug('RAJADA_TRACKER - No response for UdpTrackerAnnounce: %s %s' % (ip, port))
			return None
		if b"Connection ID missmatch" in response:
			#log.debug('RAJADA_TRACKER - Connection ID missmatch at socket response')
			return None

		try:
		    tracker_announce_output = UdpTrackerAnnounceOutput()
		    tracker_announce_output.from_bytes(response)
		    return (tracker_announce_output.seeders, tracker_announce_output.leechers)
		except Exception as e:
			#xbmcgui.Dialog().ok('Rajada Tracker', 'announce output fail\n%s %s\n%s' % (ip, port, repr(e)))
			#log.debug('RAJADA_TRACKER - UdpTrackerAnnounceOutput from_bytes() failed')
			return None

	return None
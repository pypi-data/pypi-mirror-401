# Auto generate by AUTO-GENERATE script
import enum
import socket


class AddressFamily(enum.IntEnum):
	AppleTalk = socket.AF_APPLETALK
	Bluetooth = socket.AF_BLUETOOTH
	HyperV = socket.AF_HYPERV
	Inet = socket.AF_INET
	Inet6 = socket.AF_INET6
	IPX = socket.AF_IPX
	IrDA = socket.AF_IRDA
	Link = socket.AF_LINK
	SNA = socket.AF_SNA
	UnSpec = socket.AF_UNSPEC


class AddressInfoFlags(enum.IntFlag):
	Addrconfig = socket.AI_ADDRCONFIG
	All = socket.AI_ALL
	Canonname = socket.AI_CANONNAME
	NumericHost = socket.AI_NUMERICHOST
	Numericserv = socket.AI_NUMERICSERV
	Passive = socket.AI_PASSIVE
	V4Mapped = socket.AI_V4MAPPED


class BluetoothAddress(enum.IntEnum):
	Any = socket.BDADDR_ANY
	Local = socket.BDADDR_LOCAL


class BluetoothProtocol(enum.IntEnum):
	Rfcomm = socket.BTPROTO_RFCOMM


class AddressInfo(enum.IntEnum):
	Again = socket.EAI_AGAIN
	BadFlags = socket.EAI_BADFLAGS
	Fail = socket.EAI_FAIL
	Family = socket.EAI_FAMILY
	Memory = socket.EAI_MEMORY
	Nodata = socket.EAI_NODATA
	Noname = socket.EAI_NONAME
	Service = socket.EAI_SERVICE
	SockType = socket.EAI_SOCKTYPE


class HyperVSocket(enum.IntEnum):
	AddressFlagPassthru = socket.HVSOCKET_ADDRESS_FLAG_PASSTHRU
	ConnectedSuspend = socket.HVSOCKET_CONNECTED_SUSPEND
	ConnectTimeout = socket.HVSOCKET_CONNECT_TIMEOUT
	ConnectTimeoutMax = socket.HVSOCKET_CONNECT_TIMEOUT_MAX


class HyperV(enum.IntEnum):
	GuidBroadcast = socket.HV_GUID_BROADCAST
	GuidChildren = socket.HV_GUID_CHILDREN
	GuidLoopback = socket.HV_GUID_LOOPBACK
	GuidParent = socket.HV_GUID_PARENT
	GuidWildcard = socket.HV_GUID_WILDCARD
	GuidZero = socket.HV_GUID_ZERO
	ProtocolRaw = socket.HV_PROTOCOL_RAW


class InternetAddress(enum.IntEnum):
	AllhostsGroup = socket.INADDR_ALLHOSTS_GROUP
	Any = socket.INADDR_ANY
	Broadcast = socket.INADDR_BROADCAST
	Loopback = socket.INADDR_LOOPBACK
	MaxLocalGroup = socket.INADDR_MAX_LOCAL_GROUP
	NoneAddr = socket.INADDR_NONE
	UnspecGroup = socket.INADDR_UNSPEC_GROUP


class IPPort(enum.IntEnum):
	Reserved = socket.IPPORT_RESERVED
	Userreserved = socket.IPPORT_USERRESERVED


class IPProtocol(enum.IntEnum):
	Ah = socket.IPPROTO_AH
	Cbt = socket.IPPROTO_CBT
	Dstopts = socket.IPPROTO_DSTOPTS
	Egp = socket.IPPROTO_EGP
	Esp = socket.IPPROTO_ESP
	Fragment = socket.IPPROTO_FRAGMENT
	Ggp = socket.IPPROTO_GGP
	Hopopts = socket.IPPROTO_HOPOPTS
	Iclfxbm = socket.IPPROTO_ICLFXBM
	Icmp = socket.IPPROTO_ICMP
	Icmpv6 = socket.IPPROTO_ICMPV6
	Idp = socket.IPPROTO_IDP
	Igmp = socket.IPPROTO_IGMP
	Igp = socket.IPPROTO_IGP
	Ip = socket.IPPROTO_IP
	Ipv4 = socket.IPPROTO_IPV4
	Ipv6 = socket.IPPROTO_IPV6
	L2Tp = socket.IPPROTO_L2TP
	Max = socket.IPPROTO_MAX
	Nd = socket.IPPROTO_ND
	NoneAddr = socket.IPPROTO_NONE
	Pgm = socket.IPPROTO_PGM
	Pim = socket.IPPROTO_PIM
	Pup = socket.IPPROTO_PUP
	Raw = socket.IPPROTO_RAW
	Rdp = socket.IPPROTO_RDP
	Routing = socket.IPPROTO_ROUTING
	Sctp = socket.IPPROTO_SCTP
	St = socket.IPPROTO_ST
	TCP = socket.IPPROTO_TCP
	UDP = socket.IPPROTO_UDP


class IPv6Options(enum.IntEnum):
	Checksum = socket.IPV6_CHECKSUM
	Dontfrag = socket.IPV6_DONTFRAG
	Hoplimit = socket.IPV6_HOPLIMIT
	Hopopts = socket.IPV6_HOPOPTS
	JoinGroup = socket.IPV6_JOIN_GROUP
	LeaveGroup = socket.IPV6_LEAVE_GROUP
	MulticastHops = socket.IPV6_MULTICAST_HOPS
	MulticastIf = socket.IPV6_MULTICAST_IF
	MulticastLoop = socket.IPV6_MULTICAST_LOOP
	Pktinfo = socket.IPV6_PKTINFO
	Recvrthdr = socket.IPV6_RECVRTHDR
	Recvtclass = socket.IPV6_RECVTCLASS
	Rthdr = socket.IPV6_RTHDR
	Tclass = socket.IPV6_TCLASS
	UnicastHops = socket.IPV6_UNICAST_HOPS
	V6Only = socket.IPV6_V6ONLY


class IPOptions(enum.IntEnum):
	AddMembership = socket.IP_ADD_MEMBERSHIP
	AddSourceMembership = socket.IP_ADD_SOURCE_MEMBERSHIP
	BlockSource = socket.IP_BLOCK_SOURCE
	DropMembership = socket.IP_DROP_MEMBERSHIP
	DropSourceMembership = socket.IP_DROP_SOURCE_MEMBERSHIP
	Hdrincl = socket.IP_HDRINCL
	MulticastIf = socket.IP_MULTICAST_IF
	MulticastLoop = socket.IP_MULTICAST_LOOP
	MulticastTtl = socket.IP_MULTICAST_TTL
	Options = socket.IP_OPTIONS
	Pktinfo = socket.IP_PKTINFO
	Recvdstaddr = socket.IP_RECVDSTADDR
	Recvtos = socket.IP_RECVTOS
	Tos = socket.IP_TOS
	Ttl = socket.IP_TTL
	UnblockSource = socket.IP_UNBLOCK_SOURCE


class MessageFlags(enum.IntFlag):
	Boardcast = socket.MSG_BCAST
	Ctrunc = socket.MSG_CTRUNC
	DontRoute = socket.MSG_DONTROUTE
	ErrorQueue = socket.MSG_ERRQUEUE
	Multicast = socket.MSG_MCAST
	OOB = socket.MSG_OOB
	Peek = socket.MSG_PEEK
	Truncate = socket.MSG_TRUNC
	WaitAll = socket.MSG_WAITALL


class NameInfoFlags(enum.IntFlag):
	UDP = socket.NI_DGRAM
	MaxHost = socket.NI_MAXHOST
	Maxserv = socket.NI_MAXSERV
	NameReqD = socket.NI_NAMEREQD
	NoFQDN = socket.NI_NOFQDN
	NumericHost = socket.NI_NUMERICHOST
	Numericserv = socket.NI_NUMERICSERV


class ReceiveAll(enum.IntEnum):
	Max = socket.RCVALL_MAX
	Off = socket.RCVALL_OFF
	On = socket.RCVALL_ON
	SocketLevelOnly = socket.RCVALL_SOCKETLEVELONLY


class ShutdownHow(enum.IntEnum):
	RD = socket.SHUT_RD
	RDWR = socket.SHUT_RDWR
	WR = socket.SHUT_WR


class SocketIOControl(enum.IntEnum):
	KeepAliveVals = socket.SIO_KEEPALIVE_VALS
	LoopbackFastPath = socket.SIO_LOOPBACK_FAST_PATH
	Rcvall = socket.SIO_RCVALL


class SocketKind(enum.IntEnum):
	UDP = socket.SOCK_DGRAM
	Raw = socket.SOCK_RAW
	Rdm = socket.SOCK_RDM
	SeqPacket = socket.SOCK_SEQPACKET
	TCP = socket.SOCK_STREAM


class SocketLevel(enum.IntEnum):
	Ip = socket.SOL_IP
	Socket = socket.SOL_SOCKET
	TCP = socket.SOL_TCP
	UDP = socket.SOL_UDP


class SocketOptions(enum.IntEnum):
	AcceptConn = socket.SO_ACCEPTCONN
	Broadcast = socket.SO_BROADCAST
	Debug = socket.SO_DEBUG
	DontRoute = socket.SO_DONTROUTE
	Error = socket.SO_ERROR
	ExclusiveAddrUse = socket.SO_EXCLUSIVEADDRUSE
	KeepAlive = socket.SO_KEEPALIVE
	Linger = socket.SO_LINGER
	OOBInline = socket.SO_OOBINLINE
	RcvBuf = socket.SO_RCVBUF
	RcvLowat = socket.SO_RCVLOWAT
	RcvTimeout = socket.SO_RCVTIMEO
	ReuseAddr = socket.SO_REUSEADDR
	SndBuf = socket.SO_SNDBUF
	SndLowat = socket.SO_SNDLOWAT
	SndTimeout = socket.SO_SNDTIMEO
	Type = socket.SO_TYPE
	UseLoopback = socket.SO_USELOOPBACK


class TCPOptions(enum.IntEnum):
	FastOpen = socket.TCP_FASTOPEN
	KeepCnt = socket.TCP_KEEPCNT
	KeepIDLE = socket.TCP_KEEPIDLE
	KeepIntvl = socket.TCP_KEEPINTVL
	MaxSegment = socket.TCP_MAXSEG
	NoDelay = socket.TCP_NODELAY



from enum import IntEnum


class StatuCode(IntEnum):
    """HTTP status codes and reason phrases
    Status codes from the following RFCs are all observed:
        * RFC 7231: Hypertext Transfer Protocol (HTTP/1.1), obsoletes 2616
        * RFC 6585: Additional HTTP Status Codes
        * RFC 3229: Delta encoding in HTTP
        * RFC 4918: HTTP Extensions for WebDAV, obsoletes 2518
        * RFC 5842: Binding Extensions to WebDAV
        * RFC 7238: Permanent Redirect
        * RFC 2295: Transparent Content Negotiation in HTTP
        * RFC 2774: An HTTP Extension Framework
        * RFC 7540: Hypertext Transfer Protocol Version 2 (HTTP/2)
        * RFC 2324: Hyper Text Coffee Pot Control Protocol (HTCPCP/1.0)
        * RFC 7725: An HTTP Status Code to Report Legal Obstacles
    """

    def __new__(cls, value: int, phrase: str = "") -> "StatuCode":
        obj = int.__new__(cls, value)  # type: ignore
        obj._value_ = value

        obj.phrase = phrase
        return obj

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def get_reason_phrase(cls, value: int) -> str:
        try:
            return StatuCode(value).phrase  # type: ignore
        except ValueError:
            return ""

    @classmethod
    def is_redirect(cls, value: int) -> bool:
        return value in (
            # 301 (Cacheable redirect. Method may change to GET.)
            StatuCode.MOVED_PERMANENTLY,
            # 302 (Uncacheable redirect. Method may change to GET.)
            StatuCode.FOUND,
            # 303 (Client should make a GET or HEAD request.)
            StatuCode.SEE_OTHER,
            # 307 (Equiv. 302, but retain method)
            StatuCode.TEMPORARY_REDIRECT,
            # 308 (Equiv. 301, but retain method)
            StatuCode.PERMANENT_REDIRECT,
        )

    @classmethod
    def is_error(cls, value: int) -> bool:
        return 400 <= value <= 599

    @classmethod
    def is_client_error(cls, value: int) -> bool:
        return 400 <= value <= 499

    @classmethod
    def is_server_error(cls, value: int) -> bool:
        return 500 <= value <= 599

    # informational
    CONTINUE = 100, "Continue"
    SWITCHING_PROTOCOLS = 101, "Switching Protocols"
    PROCESSING = 102, "Processing"

    # success
    OK = 200, "OK"
    CREATED = 201, "Created"
    ACCEPTED = 202, "Accepted"
    NON_AUTHORITATIVE_INFORMATION = 203, "Non-Authoritative Information"
    NO_CONTENT = 204, "No Content"
    RESET_CONTENT = 205, "Reset Content"
    PARTIAL_CONTENT = 206, "Partial Content"
    MULTI_STATUS = 207, "Multi-Status"
    ALREADY_REPORTED = 208, "Already Reported"
    IM_USED = 226, "IM Used"

    # redirection
    MULTIPLE_CHOICES = 300, "Multiple Choices"
    MOVED_PERMANENTLY = 301, "Moved Permanently"
    FOUND = 302, "Found"
    SEE_OTHER = 303, "See Other"
    NOT_MODIFIED = 304, "Not Modified"
    USE_PROXY = 305, "Use Proxy"
    TEMPORARY_REDIRECT = 307, "Temporary Redirect"
    PERMANENT_REDIRECT = 308, "Permanent Redirect"

    # client error
    BAD_REQUEST = 400, "Bad Request"
    UNAUTHORIZED = 401, "Unauthorized"
    PAYMENT_REQUIRED = 402, "Payment Required"
    FORBIDDEN = 403, "Forbidden"
    NOT_FOUND = 404, "Not Found"
    METHOD_NOT_ALLOWED = 405, "Method Not Allowed"
    NOT_ACCEPTABLE = 406, "Not Acceptable"
    PROXY_AUTHENTICATION_REQUIRED = 407, "Proxy Authentication Required"
    REQUEST_TIMEOUT = 408, "Request Timeout"
    CONFLICT = 409, "Conflict"
    GONE = 410, "Gone"
    LENGTH_REQUIRED = 411, "Length Required"
    PRECONDITION_FAILED = 412, "Precondition Failed"
    REQUEST_ENTITY_TOO_LARGE = 413, "Request Entity Too Large"
    REQUEST_URI_TOO_LONG = 414, "Request-URI Too Long"
    UNSUPPORTED_MEDIA_TYPE = 415, "Unsupported Media Type"
    REQUESTED_RANGE_NOT_SATISFIABLE = 416, "Requested Range Not Satisfiable"
    EXPECTATION_FAILED = 417, "Expectation Failed"
    IM_A_TEAPOT = 418, "I'm a teapot"
    MISDIRECTED_REQUEST = 421, "Misdirected Request"
    UNPROCESSABLE_ENTITY = 422, "Unprocessable Entity"
    LOCKED = 423, "Locked"
    FAILED_DEPENDENCY = 424, "Failed Dependency"
    UPGRADE_REQUIRED = 426, "Upgrade Required"
    PRECONDITION_REQUIRED = 428, "Precondition Required"
    TOO_MANY_REQUESTS = 429, "Too Many Requests"
    REQUEST_HEADER_FIELDS_TOO_LARGE = 431, "Request Header Fields Too Large"
    UNAVAILABLE_FOR_LEGAL_REASONS = 451, "Unavailable For Legal Reasons"

    # server errors
    INTERNAL_SERVER_ERROR = 500, "Internal Server Error"
    NOT_IMPLEMENTED = 501, "Not Implemented"
    BAD_GATEWAY = 502, "Bad Gateway"
    SERVICE_UNAVAILABLE = 503, "Service Unavailable"
    GATEWAY_TIMEOUT = 504, "Gateway Timeout"
    HTTP_VERSION_NOT_SUPPORTED = 505, "HTTP Version Not Supported"
    VARIANT_ALSO_NEGOTIATES = 506, "Variant Also Negotiates"
    INSUFFICIENT_STORAGE = 507, "Insufficient Storage"
    LOOP_DETECTED = 508, "Loop Detected"
    NOT_EXTENDED = 510, "Not Extended"
    NETWORK_AUTHENTICATION_REQUIRED = 511, "Network Authentication Required"


status_codes = StatuCode

#  Include lower-case styles for `requests` compatibility.
for code in status_codes:
    setattr(status_codes, code._name_.lower(), int(code))


class TraceCode(IntEnum):
    def __new__(cls, value: int, phrase: str = "") -> "TraceCode":
        obj = int.__new__(cls, value)  # type: ignore
        obj._value_ = value

        obj.phrase = phrase
        return obj

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def get_reason_phrase(cls, value: int) -> str:
        try:
            return TraceCode(value).phrase  # type: ignore
        except ValueError:
            return ""

    @classmethod
    def is_400_bad_request(cls, value: int) -> bool:
        return value in (
            TraceCode.PARAM_ENTRY_101_ERROR,
            TraceCode.VALIDATION_102_ERROR,
            TraceCode.USERNAME_PASSWORD_103_ERROR,
            TraceCode.OBS_ACCESS_104_ERROR,
            TraceCode.AISHU_HUB_ACCESS_105_ERROR,
            TraceCode.DATA_INTEGRATION_113_ERROR,
        )

    @classmethod
    def is_401_unauthorized(cls, value: int) -> bool:
        return value in (
            TraceCode.INVALID_USER_SESSION_106,
            TraceCode.INVALID_SERVER_SIGNATURE_107,
        )

    @classmethod
    def is_403_forbinden(cls, value: int) -> bool:
        return value in (
            TraceCode.AUTH_108_ERROR,
        )

    @classmethod
    def is_404_not_found(cls, value: int) -> bool:
        return value in (
            TraceCode.DATA_NOT_FOUND_109,
        )

    @classmethod
    def is_409_conflict(cls, value: int) -> bool:
        return value in (
            TraceCode.DATA_ALREADY_MODIFIED_110,
            TraceCode.DATA_ALREADY_EXIST_111,
        )

    @classmethod
    def is_500_internal_server_error(cls, value: int) -> bool:
        return value in (
            TraceCode.INTERNAL_SERVER_112_ERROR,
        )

    SUCCESS = 100, "success"
    PARAM_ENTRY_101_ERROR = 101, "necessary parameter is not entered"
    VALIDATION_102_ERROR = 102, "parameters are invalid"
    USERNAME_PASSWORD_103_ERROR = 103, "The username or password is incorrect"
    OBS_ACCESS_104_ERROR = 104, "OBS access error"
    AISHU_HUB_ACCESS_105_ERROR = 105, "AISHU HUB access error"
    INVALID_USER_SESSION_106 = 106, "access_token is invalid"
    INVALID_SERVER_SIGNATURE_107 = 107, "invalid client_id or client_secret"
    AUTH_108_ERROR = 108, "Forbidden"
    DATA_NOT_FOUND_109 = 109, "Data Not Found"
    DATA_ALREADY_MODIFIED_110 = 110, "Data Already Modified"
    DATA_ALREADY_EXIST_111 = 111, "Data Already Exist"
    INTERNAL_SERVER_112_ERROR = 112, "Internal server error"
    DATA_INTEGRATION_113_ERROR = 113, "Data integration error"
    OIDC_CALLBACK_114_ERROR = 114, "OIDC CallBack error"
    BASIC_AUTH_115_ERROR = 115, "Incorrect email or password"

    AUTH_CLIENT_PERMISSION_DENIED_150_ERROR = 150, "Your client permission " \
                                                   "denied "
    AUTH_IP_NOT_IN_LIST_151_ERROR = 151, "Your ip add is not white list"
    AUTH_INVALID_ONETIMETOKEN_152_ERROR = 152, "Invalid onetimeToken"
    AUTH_INVALID_ONETIMETOKENSTRUCTURE_153_ERROR = 153, "Invalid " \
                                                        "onetimeToken " \
                                                        "structure "
    AUTH_INVALID_ONETIMETOKEN_EXPIRED_154_ERROR = 154, "OnetimeToken expired"
    AUTH_INVALID_ACCESSTOKEN_155_ERROR = 155, "Invalid accessToken"
    AUTH_INVALID_ACCESSTOKENSTRUCTURE_156_ERROR = 156, "Invalid accessToken " \
                                                       "structure "
    AUTH_INVALID_ACCESSTOKEN_EXPIRED_157_ERROR = 157, "AccessToken expired"
    AUTH_INVALID_USERTYPE_158_ERROR = 158, "Invalid userType"

    AUTH_INVALID_USEID_159_ERROR = 159, "Invalid userId"

    UNHANDLED_HTTP_EXCEPTION = 65534, "Unhandled http exception"
    UNHANDLED_SYSTEM_EXCEPTION = 65535, "Unhandled system exception"


trace_codes = TraceCode

#  Include lower-case styles for `requests` compatibility.
for code in trace_codes:
    setattr(trace_codes, code._name_.lower(), int(code))

HTTPEXCEPTION_DEFAULT_HEADER = {"WWW-Authenticate": "Bearer"}

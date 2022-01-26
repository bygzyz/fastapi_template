import shortuuid
import uuid


def get_uuid(name=None):
    # If no name is given, generate a random UUID.
    if name is None:
        return uuid.uuid4()
    elif name.lower().startswith(("http://", "https://")):
        return uuid.uuid5(uuid.NAMESPACE_URL, name)
    else:
        return uuid.uuid5(uuid.NAMESPACE_DNS, name)


def get_uuid_short(name=None):
    return shortuuid.uuid(name)


def get_uuid_decimal(name=None):
    su = shortuuid.ShortUUID(alphabet="1234567890")  #
    return '1' + su.uuid()  # always start with 1 to avoid padding


def get_uuid_no_hyphen(name=None):
    uid = str(get_uuid(name))
    suid = ''.join(uid.split('-'))
    return suid

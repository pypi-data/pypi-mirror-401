import datetime
import json
import os


SSO_TOKEN_DIR = os.path.expanduser(
    os.path.join('~', '.aws', 'sso', 'cache')
)

def _serialize_utc_timestamp(obj):
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
    return obj


def sso_json_dumps(obj):
    return json.dumps(obj, default=_serialize_utc_timestamp)
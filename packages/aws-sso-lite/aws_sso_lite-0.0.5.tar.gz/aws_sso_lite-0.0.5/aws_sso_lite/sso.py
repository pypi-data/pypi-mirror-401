from datetime import datetime, timezone
from itertools import chain
from logging import getLogger
import time
import boto3
from .utils import SSO_TOKEN_DIR, sso_json_dumps
from .vendored.botocore.utils import SSOTokenFetcher
import botocore.session
from botocore.credentials import JSONFileCache
from botocore.utils import SSOTokenLoader
from botocore.exceptions import SSOTokenLoadError, SlowDownException, AuthorizationPendingException, ExpiredTokenException

logger = getLogger(__name__)

bc_session = botocore.session.Session()

class AWSSSO:
    def __init__(self, start_url:str, sso_region:str):
        self._start_url = start_url
        self._sso_region = sso_region

        self._token_fetcher = SSOTokenFetcher(
            sso_region=sso_region,
            client_creator=bc_session.create_client,
            cache=JSONFileCache(SSO_TOKEN_DIR, dumps_func=sso_json_dumps)
        )
        registration = self._token_fetcher._registration()
        self._client_id = registration['clientId']
        self._client_secret = registration['clientSecret']

        boto3_session = boto3.session.Session(region_name=sso_region)

        self.sso_oidc_client = boto3_session.client('sso-oidc')
        self.sso_client = boto3_session.client('sso')

    def _get_cache_key(self):
        """Generate cache key including access token to auto-invalidate on token change"""
        access_token = self._get_sso_access_token()
        # If no token, use a fixed key (cache will be empty anyway)
        token_part = hash(access_token) if access_token else 'no-token'
        return hash(f'{self._start_url}::{self._sso_region}::{token_part}')

    
    def start_device_authorization(self):
        return self.sso_oidc_client.start_device_authorization(
            clientId = self._client_id,
            clientSecret = self._client_secret,
            startUrl=self._start_url
        )

    def create_token(self, device_code, store_token=True):
        retry = True
        while retry:
            retry = False
            try:
                create_token_response = self.sso_oidc_client.create_token(
                    clientId = self._client_id,
                    clientSecret = self._client_secret,
                    grantType='urn:ietf:params:oauth:grant-type:device_code',
                    deviceCode=device_code
                )

                if store_token:
                    self._token_fetcher.store_token(self._start_url, create_token_response)
                    
                return {"status":"successful"}
            except SlowDownException:
                time.sleep(5)
                retry = True
            except AuthorizationPendingException:
                return {"status":"pending"}
            except ExpiredTokenException as e:
                return {"status":"error","error": "Token expired. Please restart the authorization process."}
            
        return {"status":"error","error": "Unknown error occurred during token creation."}
    
    def get_role_credentials(self, account_id:str, role_name:str):
        access_token = self._get_sso_access_token()
        return self.sso_client.get_role_credentials(
            accessToken=access_token,
            accountId=account_id,
            roleName=role_name
        )
    
    def has_valid_access_token(self):
        access_token = self._get_sso_access_token()
        return access_token is not None

    def _get_sso_access_token(self):
        token = None
        token_loader = SSOTokenLoader(JSONFileCache(SSO_TOKEN_DIR, dumps_func=sso_json_dumps))

        try:
            token = token_loader(self._start_url)
        except SSOTokenLoadError:
            logger.debug("Token not found")
        except Exception as e:
            logger.debug(e)

        if token is None:
            return None

        expires_at = token.get('expiresAt')

        if expires_at and datetime.strptime(expires_at, '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=timezone.utc) > datetime.now(tz=timezone.utc):
            return token.get('accessToken')
        else:
            return None
    
    def get_aws_accounts(self):
        cache_key = self._get_cache_key()
        
        if cache_key in aws_accounts_cache:
            return aws_accounts_cache[cache_key]

        access_token = self._get_sso_access_token()
        accounts = list(chain.from_iterable(
                page['accountList'] 
                for page in self.sso_client.get_paginator('list_accounts').paginate(accessToken=access_token)))
        aws_accounts_cache[cache_key] = accounts
        return accounts
    
    def get_aws_account_roles(self, account_id:str):
        cache_key = f'{self._get_cache_key()}::roles::{account_id}'
        
        if cache_key in aws_account_roles_cache:
            return aws_account_roles_cache[cache_key]

        access_token = self._get_sso_access_token()
        roles = list(chain.from_iterable(
            page['roleList'] 
            for page in self.sso_client.get_paginator('list_account_roles').paginate(accessToken=access_token, accountId=account_id))
        )
        aws_account_roles_cache[cache_key] = roles
        return roles
    
    def get_account_id_by_account_name(self, account_name:str):
        accounts = self.get_aws_accounts()
        for account in accounts:
            if account.get('accountName') == account_name:
                return account.get('accountId')
        
        logger.debug(f'Account name {account_name} not found')
        return None

aws_accounts_cache = {}
aws_account_roles_cache = {}
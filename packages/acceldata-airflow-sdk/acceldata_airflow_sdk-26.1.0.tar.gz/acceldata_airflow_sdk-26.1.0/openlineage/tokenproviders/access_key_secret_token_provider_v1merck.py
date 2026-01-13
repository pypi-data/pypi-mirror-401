# Copyright 2018-2023 contributors to the OpenLineage project
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Any
import requests
from airflow.configuration import conf
from airflow.models import Variable
from dateutil import parser
from openlineage.client.transport.http import TokenProvider
from airflow.hooks.base import BaseHook
log = logging.getLogger(__name__)
# Set the environment variable to bypass proxy
os.environ["no_proxy"] = "*"
CLIENT_ID = "acceldata-app"
TOKEN_PROVIDER_PATH = "/admin/api/onboarding/token-exchange?grant_type=api_keys"
ACCELDATA_LINEAGE_URL = "acceldata_lineage_url"
ACCELDATA_LINEAGE_ENDPOINT = "acceldata_lineage_endpoint"
ACCELDATA_ACCESS_KEY = "acceldata_access_key"
ACCELDATA_SECRET_KEY = "acceldata_secret_key"
ACCELDATA_BEARER_TOKEN = "acceldata_bearer_token"
ACCELDATA_EXPIRES_AT = "acceldata_expires_at"
class AccessKeySecretKeyTokenProvider(TokenProvider):
    def __init__(self, config: dict[str, str]) -> None:
        super().__init__(config)
        log.info("AccessKeySecretKeyTokenProvider constructor invoked. Setting up the access_key and secret_Key")
        access_key_from_config = config.get("access_key")
        secret_key_from_config = config.get("secret_key")
        try:
            log.info("Try fetching connection from Airflow connection")
            conn = BaseHook.get_connection("acceldata_connection")
            log.info("Connection from Airflow connection: %s", conn.host)
            adoc_access_key = conn.login
            adoc_secret_key = conn.password
            # If either key is missing or blank, fall back to config
            if not adoc_access_key or not adoc_secret_key:
                log.info("Access or Secret key missing in Airflow connection, using config fallback.")
                if access_key_from_config and secret_key_from_config:
                    self.access_key = access_key_from_config
                    self.secret_key = secret_key_from_config
                else:
                    log.error("Even config doesn't have access_key and secret_key. Calls to ADOC will fail.")
            else:
                log.info("Found access key and secret key in connection.")
                self.access_key = adoc_access_key
                self.secret_key = adoc_secret_key
        except Exception as e:
            log.info("Unable to fetch connection from Airflow connection")
            log.info(f"Error while fetching Airflow connection: {e}")
            log.info("Falling back to config credentials.")
            if access_key_from_config and secret_key_from_config:
                self.access_key = access_key_from_config
                self.secret_key = secret_key_from_config
            else:
                log.error("Even config doesn't have access_key and secret_key. Calls to ADOC will fail.")
        # Persisting configuration from yaml
        log.info("Inside load config for the task policy")
        if self.is_config_loaded():
            log.info("Config is already loaded. Skipping loading from the config.")
        else:
            log.info("Loading the config")
            config = self.load_config()
            self.persist_config_to_airflow_variables(config)
    # Checking if the acceldata_lineage_backend_url is already available
    @staticmethod
    def is_config_loaded():
        from airflow.models import Variable
        log.info("Checking if config is already loaded")
        acceldata_lineage_url = Variable.get(ACCELDATA_LINEAGE_URL, None)
        acceldata_lineage_endpoint = Variable.get(ACCELDATA_LINEAGE_ENDPOINT, None)
        acceldata_secret_key = Variable.get(ACCELDATA_SECRET_KEY, None)
        acceldata_access_key = Variable.get(ACCELDATA_ACCESS_KEY, None)
        if acceldata_lineage_url is not None and acceldata_lineage_endpoint is not None and acceldata_secret_key is not None and acceldata_access_key is not None:
            return True
        return False
    @staticmethod
    def persist_url(transport):
        if "url" in transport:
            log.info("URL found in the transport")
            url = transport["url"]
            log.info("Caching ACCELDATA_LINEAGE_URL in Airflow variables")
            Variable.set(ACCELDATA_LINEAGE_URL, url)
            log.info("ACCELDATA_LINEAGE_URL : %s persisted inside Airflow variables.", url)
        else:
            log.error("url not found in OPENLINEAGE config")
    @staticmethod
    def persist_endpoint(transport):
        if "endpoint" in transport:
            log.info("endpoint found in the transport")
            endpoint = transport["endpoint"]
            log.info("Caching ACCELDATA_LINEAGE_ENDPOINT in Airflow variables")
            Variable.set(ACCELDATA_LINEAGE_ENDPOINT, endpoint)
            log.info("ACCELDATA_LINEAGE_ENDPOINT : %s persisted inside Airflow variables.", endpoint)
        else:
            log.error("endpoint not found in OPENLINEAGE_CONFIG")
    @staticmethod
    def persist_access_key(auth):
        if "access_key" in auth:
            log.info("endpoint found in the transport")
            access_key = auth["access_key"]
            log.info("Caching ACCELDATA_ACCESS_KEY in Airflow variables")
            Variable.set(ACCELDATA_ACCESS_KEY, access_key)
            log.info("ACCELDATA_ACCESS_KEY persisted inside Airflow variables.")
        else:
            log.error("access_key not found in OPENLINEAGE_CONFIG")
    @staticmethod
    def persist_secret_key(auth):
        if "secret_key" in auth:
            log.info("endpoint found in the transport")
            secret_key = auth["secret_key"]
            log.info("Caching the OpenLineage ACCELDATA_SECRET_KEY in Airflow variables")
            Variable.set(ACCELDATA_SECRET_KEY, secret_key)
            log.info("ACCELDATA_SECRET_KEY persisted inside Airflow variables.")
        else:
            log.error("secret_key not found in OPENLINEAGE_CONFIG")
    def load_config(self) -> Dict[str, Any]:
        log.info("Inside load_config. Trying to find the [openlineage] section in airflow.cfg.")
        try:
            # Accessing the [openlineage] section directly using conf
            openlineage_config = conf.getsection('openlineage')
            if not isinstance(openlineage_config, dict):
                log.error("Expected a dictionary for [openlineage] section but got %s", type(openlineage_config))
                return {}
            log.info("OpenLineage config: %s", openlineage_config)
            return openlineage_config
        except Exception as e:
            log.error("Error reading the airflow.cfg file: %s", e)
            return {}
    @staticmethod
    def get_bearer_token(token):
        return f"Bearer {token}"
    @staticmethod
    def _update_token_to_cache(token: str, expires_in: int):
        expiration = datetime.now() + timedelta(seconds=expires_in)
        log.info("Caching the ACCELDATA_BEARER_TOKEN and ACCELDATA_EXPIRES_AT inside airflow variables.")
        Variable.set(ACCELDATA_BEARER_TOKEN, token)
        Variable.set(ACCELDATA_EXPIRES_AT, expiration)
        log.info("Cached data successfully refreshed.")
    @staticmethod
    def _get_token_from_cache():
        log.info("Fetching the acceldata_bearer_token and its expiration time from Cache")
        cached_token = Variable.get(ACCELDATA_BEARER_TOKEN, None)
        expires_at = Variable.get(ACCELDATA_EXPIRES_AT, None)
        return cached_token, expires_at
    @staticmethod
    def validate_token(cached_token, expires_at):
        # Parse the date string into a datetime object
        if expires_at is None:
            log.warning("Token in the cache is absent.")
            return False
        else:
            log.info("Non empty expires_at")
            expires_at_date = parser.parse(expires_at)
            if cached_token is not None and expires_at_date > datetime.now():
                log.info("Token in the Cache is Valid")
                return True
            else:
                log.warning("Token from the cache has expired.")
                return False
    def _fetch_token_from_admin_central(self) -> tuple[Any, Any] | None:
        try:
            headers = {
                'Content-Type': 'application/json',  # Set the content type to JSON
            }
            data = {
                'clientId': CLIENT_ID,
                'secretKey': self.secret_key,
                'accessKey': self.access_key
            }
            token_provider_base_url = Variable.get(ACCELDATA_LINEAGE_URL, None)
            if token_provider_base_url is not None:
                token_provider_url = token_provider_base_url + TOKEN_PROVIDER_PATH
                log.info("Fetching the token from Admin Central.")
                response = requests.post(token_provider_url, json=data, headers=headers)
                log.info("Response from Admin Central Url: %s", token_provider_url)
                log.info(response)
                if response.status_code == 200:
                    log.info("Fetched the token successfully from Admin Central")
                    token_data = response.json()
                    token = token_data.get('access_token')
                    expires_in = token_data.get('expires_in')
                    expires_in_sixty_seconds_ago = expires_in - 60
                    return token, expires_in_sixty_seconds_ago
                else:
                    log.warning("Failure fetching token from Admin central API.")
                    log.warning(response.text)
                    return None, None
            else:
                log.warning("%s not present. Skipping token generation.", ACCELDATA_LINEAGE_URL)
        except Exception as e:
            log.error("Error fetching token from admin central")
    def refresh_token(self):
        log.info("Refreshing the token data.")
        token, expires_in = self._fetch_token_from_admin_central()
        if token:
            self._update_token_to_cache(token, expires_in)
        else:
            log.error("Token not found in the admin central response.")
    # To persist openlineage.yml configuration to Airflow variables
    def persist_config_to_airflow_variables(self, config):
        log.info("Inside persist_config_to_airflow_variables:")
        log.info(config)
        if "transport" in config:
            log.info("Transport found in the config")
            transport_str = config.get("transport")
            transport = json.loads(transport_str)
            log.info("Transport config as dict: %s", transport)
            self.persist_url(transport)
            self.persist_endpoint(transport)
            if "auth" in transport:
                auth = transport.get("auth")
                self.persist_access_key(auth)
                self.persist_secret_key(auth)
            else:
                log.error("auth not found in OPENLINEAGE config")
        else:
            log.error("transport not found in OPENLINEAGE config")
    def get_bearer(self):
        log.info("Checking bearer token in the cache")
        cached_token, expires_at = self._get_token_from_cache()
        is_valid_token = self.validate_token(cached_token, expires_at)
        if is_valid_token:
            return self.get_bearer_token(cached_token)
        else:
            log.info(
                "Either the token doesn't exist or has expired. Refreshing token")
            self.refresh_token()
            cached_token, expires_at = self._get_token_from_cache()
            return self.get_bearer_token(cached_token)

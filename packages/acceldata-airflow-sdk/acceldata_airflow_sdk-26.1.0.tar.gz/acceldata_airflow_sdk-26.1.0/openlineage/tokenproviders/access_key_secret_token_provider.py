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
from airflow.hooks.base import BaseHook
from airflow.models import Variable
from dateutil import parser
from openlineage.client.transport.http import TokenProvider

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
        log.debug(
            "Initializing AccessKeySecretKeyTokenProvider. Starting credential resolution."
        )
        self.access_key = config["access_key"]
        self.secret_key = config["secret_key"]

        if self.is_config_loaded():
            log.debug("Config is already loaded. Skipping loading from the config.")
        else:
            ol_config = self._load_openlineage_config()
            access_key, secret_key, credential_source, transport = (
                self._resolve_credentials(ol_config)
            )

            if not access_key or not secret_key:
                log.error(
                    "Credential resolution failed. Neither Airflow Connection nor "
                    "OpenLineage config provides valid access_key and secret_key."
                )
                return

            self._finalize_and_persist(
                transport=transport,
                access_key=access_key,
                secret_key=secret_key,
                credential_source=credential_source,
            )

    def _load_openlineage_config(self) -> dict[str, str]:
        config = self.load_config()
        return config

    def _resolve_credentials(self, config):
        transport, access_key_from_config, secret_key_from_config = (
            self.extract_transport_and_auth(config)
        )

        # Try Airflow Connection first
        try:
            log.info(
                "Attempting to load credentials from Airflow Connection: acceldata_connection"
            )
            conn = BaseHook.get_connection("acceldata_connection")

            log.debug(
                "Airflow Connection loaded successfully (host=%s)", conn.host
            )

            if conn.login and conn.password:
                log.info(
                    "Using credentials from Airflow Connection "
                    "(access_key_present=True, secret_key_present=True)"
                )
                return conn.login, conn.password, "airflow_connection", transport

            log.warning(
                "Airflow Connection credentials are incomplete "
                "(access_key_present=%s, secret_key_present=%s).",
                bool(conn.login),
                bool(conn.password),
            )

        except Exception as e:
            log.info(
                "Airflow Connection 'acceldata_connection' not available. "
                "Falling back to OpenLineage config. Details=%s",
                e,
            )

        # Fallback to OpenLineage config
        if access_key_from_config and secret_key_from_config:
            log.info(
                "Using credentials from OpenLineage config after fallback."
            )
            return access_key_from_config, secret_key_from_config, "openlineage_config", transport

        return None, None, None, None

    def _finalize_and_persist(
            self,
            *,
            transport,
            access_key: str,
            secret_key: str,
            credential_source: str,
    ):
        self.access_key = access_key
        self.secret_key = secret_key

        log.info(
            "Persisting OpenLineage configuration and resolved credentials "
            "(credential_source=%s)",
            credential_source,
        )

        self.persist_config_to_airflow_variables(
            transport, self.access_key, self.secret_key
        )

    # Checking if the acceldata_lineage_backend_url is already available
    @staticmethod
    def is_config_loaded():
        from airflow.models import Variable
        log.debug(
            "Checking OpenLineage configuration state: "
            "verifying transport (url, endpoint) and credential availability "
            "from Airflow Variables or Airflow Connection"
        )

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
            log.debug("URL found in the transport")
            url = transport["url"]
            log.info(
                "Persisting OpenLineage backend URL to Airflow Variables (%s)", url
            )
            Variable.set(ACCELDATA_LINEAGE_URL, url)
        else:
            log.error(
                "Missing required OpenLineage configuration: transport.url not found"
            )

    @staticmethod
    def persist_endpoint(transport):
        if "endpoint" in transport:
            log.debug("endpoint found in the transport")
            endpoint = transport["endpoint"]
            log.info(
                "Persisting OpenLineage endpoint to Airflow Variables (%s)", endpoint
            )
            Variable.set(ACCELDATA_LINEAGE_ENDPOINT, endpoint)
        else:
            log.error(
                "Missing required OpenLineage configuration: transport.endpoint not found"
            )

    @staticmethod
    def persist_access_key(access_key: str | None):
        if not access_key:
            log.debug(
                "access_key not provided for persistence. Skipping Airflow Variable update."
            )
            return

        log.debug("Persisting access_key to Airflow Variables")
        Variable.set(ACCELDATA_ACCESS_KEY, access_key)

    @staticmethod
    def persist_secret_key(secret_key: str | None):
        if not secret_key:
            log.debug(
                "secret_key not provided for persistence. Skipping Airflow Variable update."
            )
            return

        log.debug("Persisting secret_key to Airflow Variables")
        Variable.set(ACCELDATA_SECRET_KEY, secret_key)

    def load_config(self) -> Dict[str, Any]:
        log.debug(
            "Attempting to load [openlineage] section from airflow.cfg"
        )
        try:
            # Accessing the [openlineage] section directly using conf
            openlineage_config = conf.getsection('openlineage')
            if not isinstance(openlineage_config, dict):
                log.error(
                    "Invalid OpenLineage configuration type. "
                    "Expected dict but got %s",
                    type(openlineage_config).__name__,
                )
                return {}
            log.debug(
                "Successfully loaded OpenLineage configuration: %s",
                openlineage_config,
            )
            return openlineage_config
        except Exception as e:
            log.error(
                "Failed to read [openlineage] configuration from airflow.cfg. Error=%s",
                e,
            )
            return {}

    @staticmethod
    def get_bearer_token(token):
        return f"Bearer {token}"

    @staticmethod
    def _update_token_to_cache(token: str, expires_in: int):
        expiration = datetime.now() + timedelta(seconds=expires_in)
        log.debug(
            "Updating cached bearer token and expiry timestamp in Airflow Variables"
        )
        Variable.set(ACCELDATA_BEARER_TOKEN, token)
        Variable.set(ACCELDATA_EXPIRES_AT, expiration)
        log.debug("Bearer token cache updated successfully")

    @staticmethod
    def _get_token_from_cache():
        log.debug(
            "Fetching cached bearer token and expiry timestamp from Airflow Variables"
        )
        cached_token = Variable.get(ACCELDATA_BEARER_TOKEN, None)
        expires_at = Variable.get(ACCELDATA_EXPIRES_AT, None)
        return cached_token, expires_at

    @staticmethod
    def validate_token(cached_token, expires_at):
        # Parse the date string into a datetime object
        if expires_at is None:
            log.warning(
                "Bearer token not found in cache. Token will be generated."
            )
            return False
        else:
            expires_at_date = parser.parse(expires_at)
            if cached_token is not None and expires_at_date > datetime.now():
                log.debug("Cached bearer token is valid")
                return True
            else:
                log.warning("Cached bearer token has expired")
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
                response = requests.post(token_provider_url, json=data, headers=headers)
                log.info(
                    "Requesting bearer token from Admin Central "
                    "(url=%s, clientId=%s)",
                    token_provider_url,
                    CLIENT_ID,
                )
                log.info(response)
                if response.status_code == 200:
                    log.info("Bearer token successfully retrieved from Admin Central")
                    token_data = response.json()
                    token = token_data.get('access_token')
                    expires_in = token_data.get('expires_in')
                    expires_in_sixty_seconds_ago = expires_in - 60
                    return token, expires_in_sixty_seconds_ago
                else:
                    log.error(
                        "Failed to fetch bearer token from Admin Central "
                        "(status_code=%s, response_body=%s)",
                        response.status_code,
                        response.text,
                    )
                    return None, None
            else:
                log.warning(
                    "OpenLineage backend URL (%s) is not configured in Airflow Variables. "
                    "Token generation cannot proceed without this value.",
                    ACCELDATA_LINEAGE_URL,
                )
        except Exception as e:
            log.error(
                "Exception occurred while fetching bearer token from Admin Central. Error=%s",
                e,
            )

    def refresh_token(self):
        log.info("Refreshing bearer token")
        token, expires_in = self._fetch_token_from_admin_central()
        if token:
            self._update_token_to_cache(token, expires_in)
        else:
            log.error("Bearer token refresh failed")

    @staticmethod
    def extract_transport_and_auth(config):
        """
        Extract transport config along with access_key and secret_key (if present)
        from OpenLineage configuration.

        Returns:
            tuple[dict | None, str | None, str | None]
            -> (transport, access_key, secret_key)
        """
        if "transport" not in config:
            log.error("Missing required OpenLineage configuration: transport")
            return None, None, None

        try:
            transport = json.loads(config.get("transport"))
        except Exception as e:
            log.error("Failed to parse OpenLineage transport config. Error=%s", e)
            return None, None, None

        auth = transport.get("auth", {})
        access_key = auth.get("access_key")
        secret_key = auth.get("secret_key")

        if not access_key:
            log.debug(
                "transport.auth.access_key not found in OpenLineage config"
            )

        if not secret_key:
            log.debug(
                "transport.auth.secret_key not found in OpenLineage config"
            )

        return transport, access_key, secret_key

    # To persist the openlineage configuration to Airflow variables
    def persist_config_to_airflow_variables(self, transport, access_key, secret_key):
        log.info("Persisting OpenLineage configuration to Airflow Variables")
        self.persist_url(transport)
        self.persist_endpoint(transport)
        self.persist_access_key(access_key)
        self.persist_secret_key(secret_key)

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

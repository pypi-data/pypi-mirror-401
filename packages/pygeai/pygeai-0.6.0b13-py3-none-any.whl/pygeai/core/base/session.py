import sys
from typing import Optional

from pygeai import logger
from pygeai.core.common.config import get_settings
from pygeai.core.common.exceptions import MissingRequirementException
from pygeai.core.singleton import Singleton

settings = get_settings()


_session = None


class Session(metaclass=Singleton):
    """
    A session to store configuration state required to interact with different resources.

    :param api_key: str - API key to interact with GEAI
    :param base_url: str - Base URL of the GEAI instance
    :param eval_url: Optional[str] - Optional evaluation endpoint URL
    :param access_token: Optional[str] - OAuth access token (keyword-only)
    :param project_id: Optional[str] - Project ID for OAuth authentication (keyword-only)
    :return: Session - Instance of the Session class
    :raises: ValueError - If required parameters are missing or invalid
    """

    def __init__(
            self,
            api_key: str = None,
            base_url: str = None,
            eval_url: Optional[str] = None,
            *,
            access_token: Optional[str] = None,
            project_id: Optional[str] = None,
            alias: Optional[str] = None,
    ):
        if not api_key and not access_token:
            logger.warning("Cannot instantiate session without api_key or access_token")
        if not base_url:
            logger.warning("Cannot instantiate session without base_url")

        self.__api_key = api_key
        self.__base_url = base_url
        self.__eval_url = eval_url
        self.__access_token = access_token
        self.__project_id = project_id
        self.__alias = alias if alias else "default"

        global _session
        _session = self

    @property
    def api_key(self):
        return self.__api_key

    @api_key.setter
    def api_key(self, api_key: str):
        self.__api_key = api_key

    @property
    def base_url(self):
        return self.__base_url

    @base_url.setter
    def base_url(self, base_url: str):
        self.__base_url = base_url

    @property
    def eval_url(self):
        return self.__eval_url

    @eval_url.setter
    def eval_url(self, eval_url: str):
        self.__eval_url = eval_url

    @property
    def access_token(self):
        return self.__access_token

    @access_token.setter
    def access_token(self, access_token: str):
        self.__access_token = access_token

    @property
    def project_id(self):
        return self.__project_id

    @project_id.setter
    def project_id(self, project_id: str):
        self.__project_id = project_id

    @property
    def alias(self):
        return self.__alias

    @alias.setter
    def alias(self, alias: str):
        self.__alias = alias


def get_session(alias: str = None) -> Session:
    """
    Session is a singleton object:
    On the first invocation, returns Session configured with the API KEY and BASE URL corresponding to the
    alias provided. On the following invocations, it returns the first object instantiated.
    """
    try:
        global _session
        if _session is None:
            if not alias:
                alias = "default"
            
            _validate_alias(alias)

            _session = Session(
                api_key=settings.get_api_key(alias),
                base_url=settings.get_base_url(alias),
                eval_url=settings.get_eval_url(alias),
                access_token=settings.get_access_token(alias),
                project_id=settings.get_project_id(alias),
                alias=alias,
            )
        elif _session is not None and alias:
            _validate_alias(alias)
            
            _session.alias = alias
            _session.api_key = settings.get_api_key(alias)
            _session.base_url = settings.get_base_url(alias)
            _session.eval_url = settings.get_eval_url(alias)
            _session.access_token = settings.get_access_token(alias)
            _session.project_id = settings.get_project_id(alias)

        if alias:
            logger.debug(f"Alias: {alias}")
            logger.debug(f"Base URL: {_session.base_url}")

        return _session
    except ValueError as e:
        logger.warning(f"Warning: API_KEY and/or BASE_URL not set. {e}")
        sys.stdout.write("Warning: API_KEY and/or BASE_URL not set. Please run geai configure to set them up.\n")


def _validate_alias(alias: str):
    # Validate alias exists
    available_aliases = settings.list_aliases()
    if alias not in available_aliases:
        raise MissingRequirementException(
            f"The profile '{alias}' doesn't exist. Use 'geai configure --list' to see available profiles."
        )
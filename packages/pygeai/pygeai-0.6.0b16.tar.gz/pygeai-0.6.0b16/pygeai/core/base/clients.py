from abc import ABC
from pygeai import logger

from pygeai.core.base.session import get_session, Session
from pygeai.core.common.exceptions import MissingRequirementException
from pygeai.core.services.rest import ApiService
from pygeai.core.utils.validators import validate_status_code



class BaseClient(ABC):
    _logged_session_config = None

    def __init__(self, api_key: str = None, base_url: str = None, alias: str = None, *,
                 access_token: str = None, project_id: str = None):
        """
        If commont settings are not specified, they're retrieved from default Session, based on the
        credential files.
        :param api_key: GEAI API KEY to access services
        :param base_url: URL for GEAI instance to be used
        :param alias: Alias to use from credentials file
        :param access_token: OAuth access token (keyword-only)
        :param project_id: Project ID for OAuth authentication (keyword-only)
        """
        if access_token and not project_id:
            raise MissingRequirementException("project_id is required when using access_token")

        if not (api_key and base_url) and not (access_token and base_url) and alias:
            self.__session = get_session(alias)
            if not self.__session:
                raise MissingRequirementException("API KEY and BASE URL must be defined in order to use this functionality")
        elif (api_key or access_token) and base_url:
            self.__session = get_session()
            self.__session.api_key = api_key
            self.__session.access_token = access_token
            self.__session.project_id = project_id
            self.__session.base_url = base_url
        else:
            self.__session = get_session()

        if self.session is None:
            raise MissingRequirementException("Cannot access this functionality without setting API_KEY and BASE_URL")
        
        # Log session config only once per unique session configuration
        session_config_key = (
            self.session.alias,
            self.session.base_url,
            bool(self.session.access_token),
            bool(self.session.api_key)
        )
        
        if BaseClient._logged_session_config != session_config_key:
            if self.session.access_token and self.session.project_id:
                logger.info(f"Using OAuth 2.0 authentication")
            elif self.session.api_key:
                logger.info(f"Using API Key authentication")
            else:
                logger.warning("No authentication method configured")
            
            logger.info(f"Alias: {self.session.alias}")
            logger.info(f"Base URL: {self.session.base_url}")
            
            BaseClient._logged_session_config = session_config_key

        token = self.session.access_token if self.session.access_token else self.session.api_key
        
        self.__api_service = ApiService(
            base_url=self.session.base_url,
            token=token,
            project_id=self.session.project_id
        )

    @property
    def session(self):
        return self.__session

    @session.setter
    def session(self, session: Session):
        self.__session = session

    @property
    def api_service(self):
        return self.__api_service

    @api_service.setter
    def api_service(self, api_service: ApiService):
        self.__api_service = api_service


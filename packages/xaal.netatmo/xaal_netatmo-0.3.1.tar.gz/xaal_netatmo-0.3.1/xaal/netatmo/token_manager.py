import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class TokenManager:
    """Manages OAuth tokens for Netatmo API with automatic refresh"""

    def __init__(self, config):
        self.config = config
        self.cfg = config['config']

    def get_valid_token(self) -> Optional[str]:
        """Get access token from configuration (no validation)"""
        access_token = self.cfg.get('access_token')

        if not access_token:
            logger.error("No access_token found in configuration")
            return None

        return access_token

    def refresh_on_auth_error(self) -> bool:
        """Refresh token after authentication error"""
        logger.info("Authentication failed, attempting token refresh")
        return self._refresh_access_token()

    def _refresh_access_token(self) -> bool:
        """Refresh access token using refresh_token"""
        refresh_token = self.cfg.get('refresh_token')

        if not refresh_token:
            logger.error("No refresh_token found in configuration")
            return False

        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': self.cfg['client_id'],
            'client_secret': self.cfg['client_secret'],
        }

        try:
            response = requests.post("https://api.netatmo.com/oauth2/token", data=payload, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Check if tokens actually changed
            access_token_changed = data['access_token'] != self.cfg.get('access_token')
            refresh_token_changed = 'refresh_token' in data and data['refresh_token'] != self.cfg.get('refresh_token')

            # Update configuration only if tokens changed
            if access_token_changed or refresh_token_changed:
                self.cfg['access_token'] = data['access_token']
                if 'refresh_token' in data:
                    self.cfg['refresh_token'] = data['refresh_token']

                # Save updated configuration only when needed
                self.config.write()

                if access_token_changed:
                    logger.info("Access token refreshed")
                if refresh_token_changed:
                    logger.info("Refresh token updated")
            else:
                logger.info("Tokens unchanged (no refresh needed)")

            return True

        except requests.exceptions.RequestException as e:
            logger.error(f"Token refresh failed: {e}")
            return False
        except KeyError as e:
            logger.error(f"Invalid token refresh response: {e}")
            return False

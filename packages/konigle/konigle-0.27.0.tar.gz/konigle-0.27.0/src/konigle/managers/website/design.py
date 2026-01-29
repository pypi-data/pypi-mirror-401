from typing import TYPE_CHECKING

from konigle.logging import get_logger

if TYPE_CHECKING:
    from konigle.session import AsyncSession, SyncSession


class BaseStyleSheetManager:
    resource_class = None
    """The resource model class this manager handles."""

    base_path = "/admin/api/storefront-assets"
    """The API base path for this resource type."""

    stylesheet_asset_code = "ds-stylesheet"


class StylesheetManager(BaseStyleSheetManager):
    """Manager for managing design system stylesheet for the website."""

    def __init__(self, session: "SyncSession"):
        self._session = session
        self.logger = get_logger()
        self._asset_id: str | None = None

    def get_content(self) -> str:
        """
        Get the content of the design system stylesheet.

        Returns:
            str: The stylesheet content.
        Raises:
            ValueError: If the stylesheet asset is not found.
        """
        # first send bootstrap request to get the asset id
        asset_id = self._get_stylesheet_asset_id()
        if not asset_id:
            raise ValueError("Stylesheet asset not found")
        url = f"{self.base_path}/{asset_id}/get-file-content"
        response = self._session.get(url)
        response.raise_for_status()
        return response.text

    def set_content(self, content: str) -> None:
        """
        Set the content of the design system stylesheet.
        This will overwrite the existing content.

        Args:
            content (str): The new stylesheet content.
        Raises:
            ValueError: If the stylesheet asset is not found.
        """
        asset_id = self._get_stylesheet_asset_id()
        if not asset_id:
            raise ValueError("Stylesheet asset not found")
        url = f"{self.base_path}/{asset_id}/save-file-content"

        params = {"content": content}
        response = self._session.patch(url, data=params)
        response.raise_for_status()
        self.logger.info("✅ Stylesheet content updated successfully")

    def _get_stylesheet_asset_id(self) -> str | None:
        if self._asset_id:
            return self._asset_id
        params = {"code": self.stylesheet_asset_code}
        url = f"{self.base_path}/bootstrap"
        response = self._session.post(url, data=params)
        response.raise_for_status()
        asset = response.json()
        self._asset_id = asset.get("id")
        return self._asset_id


class AsyncStylesheetManager(BaseStyleSheetManager):
    """Asynchronous manager for managing design system stylesheet for the
    website."""

    def __init__(self, session: "AsyncSession"):
        self._session = session
        self.logger = get_logger()
        self._asset_id: str | None = None

    async def get_content(self) -> str:
        """
        Get the content of the design system stylesheet.

        Returns:
            str: The stylesheet content.
        Raises:
            ValueError: If the stylesheet asset is not found.
        """
        # first send bootstrap request to get the asset id
        asset_id = await self._get_stylesheet_asset_id()
        if not asset_id:
            raise ValueError("Stylesheet asset not found")
        url = f"{self.base_path}/{asset_id}/get-file-content"
        response = await self._session.get(url)
        response.raise_for_status()
        return response.text

    async def set_content(self, content: str) -> None:
        """
        Set the content of the design system stylesheet.
        This will overwrite the existing content.

        Args:
            content (str): The new stylesheet content.
        Raises:
            ValueError: If the stylesheet asset is not found.
        """
        asset_id = await self._get_stylesheet_asset_id()
        if not asset_id:
            raise ValueError("Stylesheet asset not found")
        url = f"{self.base_path}/{asset_id}/save-file-content"
        params = {"content": content}
        response = await self._session.patch(url, data=params)
        response.raise_for_status()
        self.logger.info("✅ Stylesheet content updated successfully")

    async def _get_stylesheet_asset_id(self) -> str | None:
        if self._asset_id:
            return self._asset_id
        params = {"code": self.stylesheet_asset_code}
        url = f"{self.base_path}/bootstrap"
        response = await self._session.post(url, data=params)
        response.raise_for_status()
        asset = response.json()
        self._asset_id = asset.get("id")
        return self._asset_id


class BaseThemeManager:
    resource_class = None
    """The resource model class this manager handles."""

    base_path = "/themes/api/v1/site-themes"
    """The API base path for this resource type."""


class ThemeManager(BaseThemeManager):
    """Manager for managing themes for the website."""

    def __init__(self, session: "SyncSession"):
        self._session = session
        self.logger = get_logger()

    def get_theme_css(self) -> str:
        """
        Get the theme css content for the website if set.

        Returns:
            str: The theme CSS content. Empty string if no theme is set.
        """
        url = f"{self.base_path}/css"

        try:
            response = self._session.get(url)
            response.raise_for_status()
            return response.text
        except Exception:
            return ""

    def set_theme_css(self, css_content: str, backup: bool = False) -> None:
        """
        Set the theme CSS content for the website.

        Args:
            css_content (str): The new theme CSS content.
            backup (bool): Whether to create a backup of the existing CSS
            before updating.
        Raises:
        """
        url = f"{self.base_path}/css"
        payload = {"content": css_content, "backup": backup}
        response = self._session.post(url, json=payload)
        response.raise_for_status()
        self.logger.info("✅ Theme CSS updated successfully")

    def get_reference_theme_template(self) -> str:
        """
        Get the reference page for the current theme.

        Returns:
            str: The reference page URL or identifier.
        """
        url = f"{self.base_path}/reference-html"
        try:
            response = self._session.get(url)
            response.raise_for_status()
            return response.text
        except Exception:
            return ""


class AsyncThemeManager(BaseThemeManager):
    """Asynchronous manager for managing themes for the website."""

    def __init__(self, session: "AsyncSession"):
        self._session = session
        self.logger = get_logger()

    async def get_theme_css(self) -> str:
        """
        Get the theme css content for the website if set.

        Returns:
            str: The theme CSS content. Empty string if no theme is set.
        """
        url = f"{self.base_path}/css"

        try:
            response = await self._session.get(url)
            response.raise_for_status()
            return response.text
        except Exception:
            return ""

    async def set_theme_css(
        self, css_content: str, backup: bool = False
    ) -> None:
        """
        Set the theme CSS content for the website.

        Args:
            css_content (str): The new theme CSS content.
            backup (bool): Whether to create a backup of the existing CSS
            before updating.
        Raises:
        """
        url = f"{self.base_path}/css"
        payload = {"content": css_content, "backup": backup}
        response = await self._session.post(url, json=payload)
        response.raise_for_status()
        self.logger.info("✅ Theme CSS updated successfully")

    async def get_reference_theme_template(self) -> str:
        """
        Get the reference page for the current theme.
        Returns:
            str: The reference page URL or identifier.
        """
        url = f"{self.base_path}/reference-html"

        try:
            response = await self._session.get(url)
            response.raise_for_status()
            return response.text
        except Exception:
            return ""

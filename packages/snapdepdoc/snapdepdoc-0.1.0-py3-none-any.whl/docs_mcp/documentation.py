"""Documentation fetcher for various ecosystems."""

import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class DocumentationFetcher:
    """Fetch documentation URLs for libraries across different ecosystems."""

    DOCUMENTATION_SOURCES = {
        "python": {
            "pypi": "https://pypi.org/project/{library}/{version}/",
            "docs_pattern": "https://{library}.readthedocs.io/en/{version}/",
            "api_pattern": "https://{library}.readthedocs.io/en/{version}/api.html",
        },
        "npm": {
            "npm": "https://www.npmjs.com/package/{library}/v/{version}",
            "docs_pattern": "https://{library}.github.io/",
        },
        "maven": {
            "mvn": "https://mvnrepository.com/artifact/{library}/{version}",
            "docs_pattern": "https://javadoc.io/doc/{library}/{version}/",
        },
        "sbt": {
            "mvn": "https://mvnrepository.com/artifact/{library}/{version}",
            "docs_pattern": "https://javadoc.io/doc/{library}/{version}/",
            "scaladoc": "https://www.scala-lang.org/api/{version}/",
        },
    }

    async def get_documentation(
        self, library: str, version: str | None, ecosystem: str
    ) -> dict[str, Any]:
        """
        Get documentation URLs for a library.

        Args:
            library: Library name
            version: Version string (None for latest)
            ecosystem: Ecosystem identifier

        Returns:
            Dictionary with documentation URLs
        """
        if ecosystem not in self.DOCUMENTATION_SOURCES:
            return {"error": f"Unsupported ecosystem: {ecosystem}"}

        sources = self.DOCUMENTATION_SOURCES[ecosystem]
        result = {}

        # If no version specified, try to get latest
        if version is None:
            version = await self._get_latest_version(library, ecosystem)

        # Build URLs
        if "pypi" in sources:
            result["url"] = sources["pypi"].format(library=library, version=version)

        if "npm" in sources:
            result["url"] = sources["npm"].format(library=library, version=version)

        if "mvn" in sources:
            result["url"] = sources["mvn"].format(library=library, version=version)

        if "scaladoc" in sources:
            result["scaladoc"] = sources["scaladoc"].format(library=library, version=version)

        if "docs_pattern" in sources:
            result["api_reference"] = sources["docs_pattern"].format(
                library=library, version=version
            )

        if "api_pattern" in sources:
            result["api_reference"] = sources["api_pattern"].format(
                library=library, version=version
            )

        # Try to get description from package registry
        result["description"] = await self._get_package_description(library, ecosystem)

        return result

    async def search_documentation(
        self, library: str, query: str, version: str | None, ecosystem: str
    ) -> list[dict[str, str]]:
        """
        Search for API documentation within a library.

        Args:
            library: Library name
            query: Search query
            version: Version string
            ecosystem: Ecosystem identifier

        Returns:
            List of search results with URLs
        """
        # Placeholder - real implementation would use search APIs
        doc_info = await self.get_documentation(library, version, ecosystem)

        results = [
            {
                "title": f"{library} Documentation",
                "url": doc_info.get("url", ""),
                "description": f"Main documentation for {library}",
            }
        ]

        if doc_info.get("api_reference"):
            results.append(
                {
                    "title": f"{library} API Reference",
                    "url": doc_info["api_reference"],
                    "description": f"API reference for {library}",
                }
            )

        return results

    async def _get_latest_version(self, library: str, ecosystem: str) -> str:
        """
        Get the latest version of a library.

        Args:
            library: Library name
            ecosystem: Ecosystem identifier

        Returns:
            Latest version string
        """
        try:
            if ecosystem == "python":
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"https://pypi.org/pypi/{library}/json")
                    if response.status_code == 200:
                        data = response.json()
                        return data["info"]["version"]

            elif ecosystem == "npm":
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"https://registry.npmjs.org/{library}")
                    if response.status_code == 200:
                        data = response.json()
                        return data["dist-tags"]["latest"]

            elif ecosystem == "maven":
                # Maven Central API
                async with httpx.AsyncClient() as client:
                    group_id, artifact_id = library.split(":", 1)
                    url = f"https://search.maven.org/solrsearch/select?q=g:{group_id}+AND+a:{artifact_id}&rows=1&wt=json"
                    response = await client.get(url)
                    if response.status_code == 200:
                        data = response.json()
                        docs = data.get("response", {}).get("docs", [])
                        if docs:
                            return docs[0]["latestVersion"]

        except Exception as e:
            logger.warning(f"Could not fetch latest version for {library}: {e}")

        return "latest"

    async def _get_package_description(self, library: str, ecosystem: str) -> str:
        """
        Get package description from registry.

        Args:
            library: Library name
            ecosystem: Ecosystem identifier

        Returns:
            Package description
        """
        try:
            if ecosystem == "python":
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"https://pypi.org/pypi/{library}/json")
                    if response.status_code == 200:
                        data = response.json()
                        return data["info"].get("summary", "")

            elif ecosystem == "npm":
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"https://registry.npmjs.org/{library}")
                    if response.status_code == 200:
                        data = response.json()
                        return data.get("description", "")

        except Exception as e:
            logger.warning(f"Could not fetch description for {library}: {e}")

        return ""

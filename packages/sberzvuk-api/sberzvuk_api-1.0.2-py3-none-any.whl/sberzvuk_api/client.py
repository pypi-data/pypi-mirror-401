import os
import aiohttp

from typing import Any, Dict, List, Union

from .enums import Quality
from .errors import ZvukAuthError, ZvukValidationError, ZvukAPIError
from .queries import ALL_QUERIES


class ZvukAPI:
    def __init__(self, token: str):
        self._token = token
        self.base_url = "https://zvuk.com/api/v1/graphql"
        self.headers = {
                "Content-Type": "application/json",
                "X-Auth-Token": self._token,
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0 Safari/537.36"
                ),
                "Accept": "application/json",
        }


    @staticmethod
    async def get_anonymous_token() -> str:
        """shitty duplicate here, but without any headers returns 418"""
        async with aiohttp.ClientSession(
            headers={
                "Content-Type": "application/json",
                "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/124.0 Safari/537.36"
                ),
                "Accept": "application/json",
            }
        ) as session:
            try:
                async with session.get("https://zvuk.com/api/tiny/profile") as resp:
                    if resp.status != 200:
                        raise ZvukAPIError(
                            f"Failed to obtain anonymous token, status={resp.status}"
                        )
                    data = await resp.json()
                    try:
                        return data["result"]["token"]
                    except KeyError as exc:
                        raise ZvukAPIError("Unexpected response") from exc
            finally:
                await session.close()


    @classmethod
    async def create(cls, *, token: str | None = None):
        """creates new class instance with anonymous token if not provided"""
        if token is None:
            token = await cls.get_anonymous_token()
        return cls(token)


    @staticmethod
    async def download_track(url: str, dest_folder: str = ".", filename: str = "audio.mp3"):
        os.makedirs(dest_folder, exist_ok=True)

        out_path = os.path.join(dest_folder, filename)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                resp.raise_for_status()

                # check if server got file size
                total = int(resp.headers.get("content-length", 0))
                downloaded = 0

                # writing into file by chunks
                with open(out_path, "wb") as f:
                    async for chunk in resp.content.iter_chunked(8192):
                        if not chunk:
                            continue
                        f.write(chunk)
                        downloaded += len(chunk)

                        if total:
                            pct = downloaded / total * 100
                            print(f"\r{filename}: {downloaded}/{total} bytes ({pct:.1f}%)", end="")

        return out_path


    async def _execute(self, operation_name: str, variables: Dict[str, Any]):
        """just send requests with specific operation and variables"""
        if operation_name not in ALL_QUERIES:
            raise ValueError(f"Unknown operation {operation_name!r}")

        payload = {
            "operationName": operation_name,
            "variables": variables,
            "query": ALL_QUERIES[operation_name],
        }

        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                async with session.post(self.base_url, json=payload) as resp:
                    if resp.status == 401:
                        raise ZvukAuthError("Invalid or expired token")
                    if resp.status >= 400:
                        txt = await resp.text()
                        raise ZvukAPIError(f"HTTP {resp.status}: {txt}")

                    # 200 code
                    try:
                        body = await resp.json()
                    except aiohttp.ContentTypeError as exc:
                        txt = await resp.text()
                        raise ZvukAPIError(f"Non‑JSON response: {txt}") from exc

                    if "errors" in body:
                        messages = "; ".join(err.get("message", "no message")
                                              for err in body["errors"])
                        raise ZvukValidationError(messages)

                    return body.get("data", {})
            finally:
                await session.close()


    async def search(self, query: str, limit: int = 10):
        """GraphQL GetSearch"""
        data = await self._execute(
            "GetSearch",
            {"query": query, "limit": limit},
        )
        return data.get("quickSearch", {}).get("content", [])


    async def search_all(self, query: str, limit: int = 10):
        """GraphQL GetSearchAll"""
        data = await self._execute(
            "GetSearchAll",
            {"query": query, "limit": limit}
        )
        return data.get("search", {}).get('tracks').get('items')


    async def get_stream_url(self, track_id: Union[int, List[int]], quality: Quality = Quality.HIGH):
        """
        GraphQL GetStream
        returns urls for downloading tracks
        """
        ids = track_id if isinstance(track_id, list) else [track_id]
        data = await self._execute(
            "GetStream",
            {"ids": ids},
        )
        media = data.get("mediaContents", [])

        urls = []
        for item in media:
            stream = item.get("stream", {})
            if quality == Quality.HIGH and stream.get("high"):
                urls.append(stream.get("high"))
            elif quality == Quality.MID:
                urls.append(stream.get("mid"))
            else:  # fallback
                urls.append(stream.get("high") or stream.get("mid"))
        return urls


    async def get_track(self, track_id: Union[int, List[int]], with_artists: bool = False, with_album: bool = False):
        """
        GraphQL GetPlaylist
        returns info about track
        """
        ids = track_id if isinstance(track_id, list) else [track_id]
        data = await self._execute(
            "GetTracks",
            {"ids": ids, "withArtists": with_artists, "withAlbum": with_album},
        )
        return data.get("getTracks", [])


    async def get_full_track(self, track_id: Union[int, List[int]],
                             with_releases: bool = False, with_artists: bool = False):
        """
        GraphQL GetPlaylist
        returns full info about track
        """
        ids = track_id if isinstance(track_id, list) else [track_id]
        data = await self._execute(
            "GetFullTrack",
            {"ids": ids, "withReleases": with_releases, "withArtists": with_artists},
        )
        return data.get("getTracks", [])


    async def get_playlist(self, playlist_id: Union[int, List[int]]):
        """
        GraphQL GetPlaylist
        returns playlist info by playlist id
        """
        ids = playlist_id if isinstance(playlist_id, list) else [playlist_id]
        data = await self._execute(
            "GetPlaylists",
            {"ids": ids},
        )
        return data.get("playlists", [])


    async def get_album(self, album_id: int, with_artists: bool = False, with_tracks: bool = False):
        """
        GraphQL GetReleases
        returns release info by album id

        as I understand release is an official album
        """
        data = await self._execute(
            "GetReleases",
            {"ids": [album_id], "withArtists": with_artists, "withTracks": with_tracks},
        )
        return data.get("getReleases", [])


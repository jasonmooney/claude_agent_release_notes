from datetime import datetime
import os
import json

class CacheManager:
    def __init__(self, cache_dir):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_file_path(self, url):
        """Generate a cache file path based on the URL."""
        return os.path.join(self.cache_dir, self._sanitize_url(url))

    def _sanitize_url(self, url):
        """Sanitize the URL to create a valid filename."""
        return url.replace("https://", "").replace("http://", "").replace("/", "_") + ".json"

    def get_cached_data(self, url):
        """Retrieve cached data for a given URL."""
        cache_file_path = self._get_cache_file_path(url)
        if os.path.exists(cache_file_path):
            with open(cache_file_path, 'r') as cache_file:
                return json.load(cache_file)
        return None

    def cache_data(self, url, data):
        """Cache data for a given URL."""
        cache_file_path = self._get_cache_file_path(url)
        with open(cache_file_path, 'w') as cache_file:
            json.dump({
                'timestamp': datetime.utcnow().isoformat(),
                'data': data
            }, cache_file)

    def clear_cache(self):
        """Clear all cached data."""
        for filename in os.listdir(self.cache_dir):
            file_path = os.path.join(self.cache_dir, filename)
            os.remove(file_path) if os.path.isfile(file_path) else None

    def is_cache_valid(self, url, expiration_time_in_seconds):
        """Check if the cached data for a given URL is still valid."""
        cache_file_path = self._get_cache_file_path(url)
        if os.path.exists(cache_file_path):
            cache_time = datetime.fromisoformat(json.load(open(cache_file_path))['timestamp'])
            return (datetime.utcnow() - cache_time).total_seconds() < expiration_time_in_seconds
        return False
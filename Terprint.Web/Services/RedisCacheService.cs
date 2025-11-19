using System;
using System.Text.Json;
using System.Threading.Tasks;
using Microsoft.Extensions.Caching.Distributed;

namespace Terprint.Web.Services
{
    public class RedisCacheService : ICacheService
    {
        private readonly IDistributedCache _cache;
        private readonly JsonSerializerOptions _jsonOptions = new() { PropertyNameCaseInsensitive = true };

        public RedisCacheService(IDistributedCache cache)
        {
            _cache = cache;
        }

        public async Task<T?> GetAsync<T>(string key)
        {
            var data = await _cache.GetStringAsync(key);
            return data is null ? default : JsonSerializer.Deserialize<T>(data, _jsonOptions);
        }

        public async Task SetAsync<T>(string key, T value, TimeSpan? absoluteExpiration = null)
        {
            var json = JsonSerializer.Serialize(value, _jsonOptions);
            var opts = new DistributedCacheEntryOptions();
            if (absoluteExpiration.HasValue) opts.SetAbsoluteExpiration(absoluteExpiration.Value);
            await _cache.SetStringAsync(key, json, opts);
        }

        public async Task<T> GetOrCreateAsync<T>(string key, Func<Task<T>> factory, TimeSpan? ttl = null)
        {
            var cached = await GetAsync<T>(key);
            if (cached != null) return cached;
            var value = await factory();
            if (value != null) await SetAsync(key, value, ttl ?? TimeSpan.FromMinutes(10));
            return value!;
        }

        public Task RemoveAsync(string key) => _cache.RemoveAsync(key);
    }
}

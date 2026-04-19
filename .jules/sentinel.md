## 2024-05-24 - Rate Limiting DOS & Localization

**Vulnerability:** A DOS memory leak in API Server rate limiter (`gate_requests`) due to unchecked size of `_rate_state` dictionary.
**Learning:** Limiting dictionary size in memory rate limiting controls by clearing the dictionary entirely opens a rate-limiting bypass. You should use a cache TTL mechanism or pop oldest items manually.
**Prevention:** Always pop oldest elements from unbounded dictionaries instead of clearing them when adding a maximum size limit to rate-limit states.

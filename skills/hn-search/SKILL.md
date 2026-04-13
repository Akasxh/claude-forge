---
name: hn-search
description: Search Hacker News via the Algolia API -- full-text search of stories and comments, comment tree retrieval by item ID, and filtering by date range and minimum points. Use this skill IMMEDIATELY when the user asks about HN discussions, tech community sentiment, trending topics on Hacker News, or when a research dispatch needs HN data. Also use when building competitive analyses that require community discussion data, when checking what HN thinks about a project, or when gathering prior art from HN threads. This skill MUST be used instead of constructing raw HN Algolia URLs manually.
model: opus
effort: max
---

# HN Search -- Hacker News Algolia API

Encapsulates the HN Algolia REST API for structured search and retrieval of Hacker News stories, comments, and full comment trees. This is the single source of truth for all HN data access in the workforce.

## API base

All endpoints use `https://hn.algolia.com/api/v1/`.

## Method 1: Search stories and comments

### Endpoint

```
GET https://hn.algolia.com/api/v1/search?query=<text>&tags=<tags>&numericFilters=<filters>&hitsPerPage=<n>&page=<p>
```

Or for recency-ordered results:

```
GET https://hn.algolia.com/api/v1/search_by_date?query=<text>&tags=<tags>&numericFilters=<filters>&hitsPerPage=<n>&page=<p>
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | Full-text search query. Supports AND/OR/NOT and exact phrases in quotes. |
| `tags` | string | Comma-separated type filters. Values: `story`, `comment`, `poll`, `pollopt`, `show_hn`, `ask_hn`, `front_page`. Comma = AND; parentheses with comma = OR: `(story,poll)`. |
| `numericFilters` | string | Comma-separated numeric filters. Fields: `created_at_i` (Unix epoch), `points`, `num_comments`. Operators: `>`, `>=`, `<`, `<=`. Example: `points>=100,created_at_i>=1712000000` |
| `hitsPerPage` | integer | Results per page (default 20, max 1000). |
| `page` | integer | Zero-indexed page number for pagination. |

### Usage via WebFetch

```
WebFetch(
  url: "https://hn.algolia.com/api/v1/search?query=vLLM&tags=story&numericFilters=points>=50&hitsPerPage=30",
  prompt: "Extract all hits as a JSON array. For each hit return: objectID, title, url, author, points, num_comments, created_at (ISO string), and a 1-sentence summary of the title."
)
```

### Response shape

```json
{
  "hits": [
    {
      "objectID": "12345678",
      "title": "Story title",
      "url": "https://example.com/article",
      "author": "username",
      "points": 150,
      "num_comments": 42,
      "created_at": "2026-03-15T14:30:00Z",
      "created_at_i": 1773855000,
      "story_text": "Text body if Ask HN / Show HN",
      "comment_text": "Comment body if tag=comment",
      "_tags": ["story", "author_username", "story_12345678"]
    }
  ],
  "nbHits": 1200,
  "page": 0,
  "nbPages": 40,
  "hitsPerPage": 30
}
```

### Common recipes

**Search for recent discussions about a project (last 30 days):**
```
query=<project>&tags=story&numericFilters=created_at_i>=<epoch_30d_ago>&hitsPerPage=50
```
To compute epoch for 30 days ago: `date -d '30 days ago' +%s` or `$(( $(date +%s) - 2592000 ))`.

**Search for high-signal stories (100+ points):**
```
query=<topic>&tags=story&numericFilters=points>=100&hitsPerPage=50
```

**Search comments mentioning a term:**
```
query=<term>&tags=comment&hitsPerPage=50
```

**Combined: stories about X from last week with 50+ points:**
```
query=<X>&tags=story&numericFilters=points>=50,created_at_i>=<epoch_7d_ago>&hitsPerPage=50
```

**Search for Show HN or Ask HN posts:**
```
tags=show_hn&numericFilters=points>=20&hitsPerPage=30
tags=ask_hn&query=<topic>&hitsPerPage=30
```

## Method 2: Get a thread's comment tree

### Endpoint

```
GET https://hn.algolia.com/api/v1/items/<id>
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | The HN item ID (story, comment, poll). Found in `objectID` from search results or from any `news.ycombinator.com/item?id=<id>` URL. |

### Usage via WebFetch

```
WebFetch(
  url: "https://hn.algolia.com/api/v1/items/12345678",
  prompt: "Return the full comment tree. For the root item: title, author, points, num_comments, url, created_at. For each comment in the children array (recursively): author, text (first 200 chars), created_at, number of child comments. Organize as an indented tree."
)
```

### Response shape

```json
{
  "id": 12345678,
  "title": "Story title",
  "author": "username",
  "points": 150,
  "url": "https://example.com",
  "created_at": "2026-03-15T14:30:00Z",
  "children": [
    {
      "id": 12345679,
      "author": "commenter1",
      "text": "Comment HTML body...",
      "created_at": "2026-03-15T15:00:00Z",
      "children": [
        {
          "id": 12345680,
          "author": "commenter2",
          "text": "Reply HTML body...",
          "children": []
        }
      ]
    }
  ]
}
```

## Method 3: Get a specific user's submissions

### Endpoint

```
GET https://hn.algolia.com/api/v1/search?tags=story,author_<username>&hitsPerPage=50
```

This uses the tag system -- every item is tagged with `author_<username>`.

## Date arithmetic helpers

When constructing `numericFilters` with `created_at_i`, use Unix epoch seconds:

| Period | Seconds to subtract | Bash |
|--------|-------------------|------|
| 1 day | 86400 | `$(( $(date +%s) - 86400 ))` |
| 7 days | 604800 | `$(( $(date +%s) - 604800 ))` |
| 30 days | 2592000 | `$(( $(date +%s) - 2592000 ))` |
| 90 days | 7776000 | `$(( $(date +%s) - 7776000 ))` |
| 1 year | 31536000 | `$(( $(date +%s) - 31536000 ))` |

## Provenance requirements

Every HN record extracted using this skill MUST include:

1. `source_url` -- the full Algolia API URL used
2. `retrieved_at` -- ISO 8601 timestamp of the fetch
3. `extractor` -- "HN Algolia JSON via hn-search skill"

This ensures the research team's evidence chain is unbroken.

## Pagination

For queries returning more than `hitsPerPage` results, paginate by incrementing `page` from 0 to `nbPages - 1`. The response includes `nbHits` (total results) and `nbPages` (total pages). Do not fetch more than 10 pages (10,000 results) in a single research dispatch unless explicitly instructed.

## Rate limits

HN Algolia API has no published rate limit for reasonable usage. In practice:
- Stay under 1 request per second for batch fetches
- For single queries, no delay needed
- No API key required
- No authentication required

## Hard rules

- ALWAYS use HN Algolia (`hn.algolia.com/api/v1/`) for search. NEVER use the Firebase API (`hacker-news.firebaseio.com`) for search -- Firebase only returns current item data by ID and has no full-text search.
- ALWAYS use `search_by_date` when the user cares about recency. The default `search` endpoint ranks by relevance (Algolia's ranking algorithm), not by date.
- ALWAYS include provenance metadata (source_url, retrieved_at, extractor) on every record.
- NEVER fabricate HN data. If a search returns 0 results, report that -- do not invent stories or comments.
- ALWAYS use `numericFilters` for date and points thresholds. Do not attempt client-side filtering of large result sets.
- For comment trees, ALWAYS use `items/<id>` endpoint. Do not try to reconstruct trees from flat search results.

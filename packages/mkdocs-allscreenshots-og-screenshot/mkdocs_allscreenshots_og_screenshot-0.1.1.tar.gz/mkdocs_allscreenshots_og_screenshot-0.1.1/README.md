# mkdocs-allscreenshots-og-screenshot

MkDocs plugin that automatically generates dynamic OpenGraph images for every page using [Allscreenshots](https://allscreenshots.com).

Each page gets a unique `og:image` meta tag pointing to a live screenshot of that page.

## Installation
```bash
pip install mkdocs-allscreenshots-og-screenshot
```

Or install locally:
```bash
pip install -e .
```

## Usage

Add the plugin to your `mkdocs.yml`:
```yaml
site_url: https://yourdomain.com

plugins:
  - search
  - allscreenshots-og-screenshot
```

This will add the following meta tag to each page:
```html
<meta property="og:image" content="https://og.allscreenshots.com?url=https%3A%2F%2Fyourdomain.com%2Fyour-page%2F" />
```

## Configuration
```yaml
plugins:
  - allscreenshots-og-screenshot:
      screenshot_base_url: https://og.allscreenshots.com  # default
      site_url: https://yourdomain.com  # optional, falls back to site_url in mkdocs.yml
```

| Option | Default | Description |
|--------|---------|-------------|
| `screenshot_base_url` | `https://og.allscreenshots.com` | Base URL for the screenshot API |
| `site_url` | - | Override the site URL (uses `site_url` from mkdocs.yml by default) |

## License

MIT

# allscreenshots_og_screenshot/plugin.py
import re
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
from urllib.parse import urljoin, quote

class AllscreenshotsOgPlugin(BasePlugin):
    config_scheme = (
        ('screenshot_base_url', config_options.Type(str, default='https://og.allscreenshots.com')),
        ('site_url', config_options.Type(str, default='')),
    )

    def on_post_page(self, output, page, config):
        site_url = self.config['site_url'] or config.get('site_url', '').rstrip('/')
        page_url = urljoin(site_url + '/', page.url or '')
        og_image_url = f"{self.config['screenshot_base_url']}?url={quote(page_url, safe='')}"
        og_image_tag = f'<meta property="og:image" content="{og_image_url}" />'
        
        if re.search(r'<meta\s+property=["\']og:image["\']', output):
            output = re.sub(
                r'<meta\s+property=["\']og:image["\']\s+content=["\'][^"\']*["\']\s*/?>',
                og_image_tag,
                output
            )
        else:
            output = output.replace('</head>', f'  {og_image_tag}\n</head>')
        
        return output

from zen_html import H

from ...config import ZENAUTH_SERVER_CONFIG


def _is_cross_origin(url: str) -> bool:
    return url.startswith("http://") or url.startswith("https://")


def default_header_links() -> list[H]:
    cfg = ZENAUTH_SERVER_CONFIG()
    links: list[H] = []
    for href in cfg.css_list:
        if _is_cross_origin(href):
            links.append(H.link(rel="stylesheet", href=href, crossorigin="anonymous"))
        else:
            links.append(H.link(rel="stylesheet", href=href))
    return links


def default_body_links() -> list[H]:
    cfg = ZENAUTH_SERVER_CONFIG()
    links: list[H] = []
    for src in cfg.script_list:
        if _is_cross_origin(src):
            links.append(H.script(src=src, crossorigin="anonymous"))
        else:
            links.append(H.script(src=src))
    return links

# -*- coding: utf-8 -*-

"""Search the TailwindCSS Documentation"""

from os import path
import urllib.parse
import html
from algoliasearch.search_client import SearchClient
import json

from albert import *

__title__ = "TailwindCSS Docs"
__prettyname__ = "TailwindCSS Docs"
__doc__ = "Albert extension for quickly and easily searching the TailwindCSS documentation"
__version__ = "0.4.1"
__triggers__ = "tw "
__authors__ = "V13Axel (Forked from Rick West)"
__py_dep__ = ["algoliasearch"]


client = SearchClient.create("KNPXZI5B0M", "5fc87cef58bb80203d2207578309fab6")
index = client.init_index("tailwindcss")


icon = "{}/icon.png".format(path.dirname(__file__))
google_icon = "{}/google.png".format(path.dirname(__file__))

docs = "https://tailwindcss.com/docs/"


def getSubtitle(hit):
    if hit["hierarchy"]["lvl3"] is not None:
        return hit["hierarchy"]["lvl3"]

    if hit["hierarchy"]["lvl2"] is not None:
        return hit["hierarchy"]["lvl2"]

    if hit["hierarchy"]["lvl1"] is not None:
        return hit["hierarchy"]["lvl1"]

    return None


def handleQuery(query):
    items = []

    if query.isTriggered:

        if not query.isValid:
            return

        if query.string.strip():
            search = index.search(
                query.string, 
                {
                    "hitsPerPage": 5,
                    "facetFilters": [
                        'version:v3'
                    ]
                }
            )

            for hit in search["hits"]:
                title = hit["hierarchy"]["lvl0"]
                subtitle = getSubtitle(hit)
                url = hit["url"]

                items.append(
                    Item(
                        id=__prettyname__,
                        icon=icon,
                        text=html.unescape(title),
                        subtext=html.unescape(subtitle if subtitle is not None else ""),
                        actions=[UrlAction("Open in the TailwindCSS Documentation", url)],
                    )
                )

            if len(items) == 0:
                term = "tailwindcss {}".format(query.string)

                google = "https://www.google.com/search?q={}".format(
                    urllib.parse.quote(term)
                )

                items.append(
                    Item(
                        id=__prettyname__,
                        icon=google_icon,
                        text="Search Google",
                        subtext='No match found. Search Google for: "{}"'.format(term),
                        actions=[UrlAction("No match found. Search Google", google)],
                    )
                )

                items.append(
                    Item(
                        id=__prettyname__,
                        icon=icon,
                        text="Open Docs",
                        subtext="No match found. Open tailwindcss.com/docs...",
                        actions=[UrlAction("Open the TailwindCSS Documentation", docs)],
                    )
                )

        else:
            items.append(
                Item(
                    id=__prettyname__,
                    icon=icon,
                    text="Open Docs",
                    subtext="Open tailwindcss.com/docs...",
                    actions=[UrlAction("Open the TailwindCSS Documentation", docs)],
                )
            )

    return items

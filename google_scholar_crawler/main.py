"""Fetch Google Scholar stats and emit JSON files consumed by shields.io.

Produces:
  results/gs_data.json           -- full author record (publications, indices, ...)
  results/gs_data_shieldsio.json -- {schemaVersion, label, message} for the badge

The GitHub Action publishes ./results to the `google-scholar-stats` branch, so the
badge in index.html reads it via jsDelivr.
"""

import json
import os
from datetime import datetime

from scholarly import scholarly

SCHOLAR_ID = os.environ["GOOGLE_SCHOLAR_ID"]

author = scholarly.search_author_id(SCHOLAR_ID)
scholarly.fill(author, sections=["basics", "indices", "counts", "publications"])

author["updated"] = str(datetime.now())
author["publications"] = {v["author_pub_id"]: v for v in author["publications"]}

os.makedirs("results", exist_ok=True)

with open("results/gs_data.json", "w") as outfile:
    json.dump(author, outfile, ensure_ascii=False)

shieldsio_data = {
    "schemaVersion": 1,
    "label": "citations",
    "message": f"{author['citedby']}",
}

with open("results/gs_data_shieldsio.json", "w") as outfile:
    json.dump(shieldsio_data, outfile, ensure_ascii=False)

print(f"Done. {author['name']} has {author['citedby']} citations.")

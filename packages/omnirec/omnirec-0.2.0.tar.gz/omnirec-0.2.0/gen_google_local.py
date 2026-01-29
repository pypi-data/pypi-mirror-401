import os
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib import request
from urllib.request import urlretrieve

import requests

from omnirec.util.util import calculate_checksum

urls = [
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Alabama.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Alaska.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Arizona.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Arkansas.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-California.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Colorado.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Connecticut.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Delaware.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-District_of_Columbia.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Florida.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Georgia.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Hawaii.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Idaho.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Illinois.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Indiana.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Iowa.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Kansas.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Kentucky.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Louisiana.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Maine.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Maryland.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Massachusetts.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Michigan.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Minnesota.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Mississippi.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Missouri.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Montana.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Nebraska.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Nevada.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-New_Hampshire.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-New_Jersey.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-New_Mexico.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-New_York.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-North_Carolina.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-North_Dakota.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Ohio.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Oklahoma.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Oregon.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Pennsylvania.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Rhode_Island.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-South_Carolina.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-South_Dakota.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Tennessee.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Texas.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Utah.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Vermont.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Virginia.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Washington.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-West_Virginia.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Wisconsin.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/rating-Wyoming.csv.gz",
]


TEMPLATE = """elif name == "{name}":
    return DatasetInfo("{url}", "{sum}")
"""


def main():
    out = ""
    names = []

    count = 0

    for url in urls:
        print(f"{count}/{len(urls)}")
        count += 1
        url_pth = Path(url)

        new_name = "GoogleLocal2021" + url_pth.name.replace("rating-", "").replace(
            ".csv.gz", ""
        ).replace("_", "")

        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total = int(r.headers.get("content-length", 0))
            downloaded = 0
            with NamedTemporaryFile(delete=False) as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total:
                            percent = downloaded / total * 100
                            sys.stdout.write(f"\r{percent:.1f}%")
                            sys.stdout.flush()
                f.close()
                out += TEMPLATE.format(
                    name=new_name, url=url, sum=calculate_checksum(Path(f.name))
                )
                os.remove(f.name)
            names.append(new_name)

    print()
    print()
    print(out)
    print(10 * "#")
    print(names)


if __name__ == "__main__":
    main()

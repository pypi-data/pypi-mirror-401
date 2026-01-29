from pathlib import Path

import pandas as pd
from tqdm import tqdm

from omnirec.util import calculate_checksum
from yoink import dl

save_dir = Path("./yoink")

TEMPLATE = """\
elif name == \"{name}\":
    return DatasetInfo(\"{url}\", \"{sum}\")
"""


def main():
    result = ""
    names = []

    for u, num in tqdm(dl):
        save_pth = (save_dir / Path(u).name).resolve()
        if not save_pth.exists():
            raise FileNotFoundError()

        sum = calculate_checksum(save_pth)

        name = norm_name(save_pth.stem)
        result += TEMPLATE.format(name=name, url=u, sum=sum)
        names.append(name)

    print(result)
    print(10 * "#")
    print(names)


def norm_name(s: str):
    s = s.replace("ratings_", "")
    return "Amazon2014" + "".join(word.capitalize() for word in s.split("_"))


if __name__ == "__main__":
    main()

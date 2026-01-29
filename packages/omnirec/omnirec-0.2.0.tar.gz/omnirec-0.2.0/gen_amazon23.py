import hashlib
from pathlib import Path
from urllib.request import urlretrieve

links = [
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/All_Beauty.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Amazon_Fashion.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Appliances.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Arts_Crafts_and_Sewing.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Automotive.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Baby_Products.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Beauty_and_Personal_Care.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Books.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/CDs_and_Vinyl.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Cell_Phones_and_Accessories.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Clothing_Shoes_and_Jewelry.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Digital_Music.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Electronics.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Gift_Cards.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Grocery_and_Gourmet_Food.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Handmade_Products.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Health_and_Household.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Health_and_Personal_Care.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Home_and_Kitchen.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Industrial_and_Scientific.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Kindle_Store.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Magazine_Subscriptions.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Movies_and_TV.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Musical_Instruments.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Office_Products.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Patio_Lawn_and_Garden.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Pet_Supplies.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Software.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Sports_and_Outdoors.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Subscription_Boxes.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Tools_and_Home_Improvement.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Toys_and_Games.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Video_Games.csv.gz",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Unknown.csv.gz",
]


WORKING_DIR = Path("./amazon23_work")

GZ_DIR = WORKING_DIR / "gz"
GZ_DIR.mkdir(exist_ok=True, parents=True)


TEMPLATE = """\
elif name == \"{name}\":
    return DatasetInfo(\"{url}\", \"{sum}\")
"""


def calculate_checksum(file_pth: Path, chunk_size=1024 * 1024) -> str:
    hash = hashlib.sha256()
    with open(file_pth, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hash.update(chunk)
        return hash.hexdigest()


def norm_name(s: str):
    return "Amazon2023" + "".join(word.capitalize() for word in s.split("_"))


for l in links:
    p = Path(l)
    print(f'"{norm_name(Path(p.stem).stem)}",')


# Generate checksums:
# for l in links:
#     p = Path(l)
#     gz_pth = GZ_DIR / p.name

#     urlretrieve(l, gz_pth)
#     print(
#         TEMPLATE.format(
#             name=norm_name(Path(gz_pth.stem).stem),
#             url=l,
#             sum=calculate_checksum(gz_pth),
#         ),
#         end="",
#     )

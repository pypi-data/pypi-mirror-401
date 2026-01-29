from pathlib import Path

from omnirec.util.util import calculate_checksum

links = [
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/AMAZON_FASHION.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/All_Beauty.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Appliances.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Arts_Crafts_and_Sewing.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Automotive.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Books.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/CDs_and_Vinyl.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Cell_Phones_and_Accessories.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Clothing_Shoes_and_Jewelry.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Digital_Music.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Electronics.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Gift_Cards.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Grocery_and_Gourmet_Food.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Home_and_Kitchen.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Industrial_and_Scientific.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Kindle_Store.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Luxury_Beauty.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Magazine_Subscriptions.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Movies_and_TV.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Musical_Instruments.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Office_Products.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Patio_Lawn_and_Garden.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Pet_Supplies.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Prime_Pantry.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Software.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Sports_and_Outdoors.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Tools_and_Home_Improvement.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Toys_and_Games.csv",
    "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_v2/categoryFilesSmall/Video_Games.csv",
]

DS_PTH = Path("E:/data_sets")


TEMPLATE = """\
elif name == \"{name}\":
    return DatasetInfo(\"{url}\", \"{sum}\")
"""


def norm_name(s: str):
    return "Amazon2018" + "".join(word.capitalize() for word in s.split("_"))


def norm_name_lk(s: str):
    ret = "Amazon2018-" + "-".join(word.capitalize() for word in s.split("_"))
    if ret == "Amazon2018-Amazon-Fashion":
        return "Amazon2018-Fashion"
    return ret


for l in links:
    p = Path(l)
    print(f'"{norm_name(p.stem)}",')

# Generate checksums:
# for l in links:
#     p = Path(l)
#     ds_name_lk = norm_name_lk(p.stem)
#     lk_pth = DS_PTH / ds_name_lk / "source/files"

#     data_file = lk_pth.iterdir().__next__()

#     print(
#         TEMPLATE.format(
#             name=norm_name(p.stem), url=l, sum=calculate_checksum(data_file)
#         ), end="",
#     )

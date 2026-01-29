from http import HTTPStatus
from pathlib import Path
import requests
from tqdm import tqdm

dl = [
    [
        "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Books.csv",
        "ratings only (22,507,155 ratings)",
    ],
    [
        "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Electronics.csv",
        "ratings only (7,824,482 ratings)",
    ],
    [
        "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Movies_and_TV.csv",
        "ratings only (4,607,047 ratings)",
    ],
    [
        "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_CDs_and_Vinyl.csv",
        "ratings only (3,749,004 ratings)",
    ],
    [
        "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Clothing_Shoes_and_Jewelry.csv",
        "ratings only (5,748,920 ratings)",
    ],
    [
        "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Home_and_Kitchen.csv",
        "ratings only (4,253,926 ratings)",
    ],
    [
        "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Kindle_Store.csv",
        "ratings only (3,205,467 ratings)",
    ],
    [
        "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Sports_and_Outdoors.csv",
        "ratings only (3,268,695 ratings)",
    ],
    [
        "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Cell_Phones_and_Accessories.csv",
        "ratings only (3,447,249 ratings)",
    ],
    [
        "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Health_and_Personal_Care.csv",
        "ratings only (2,982,326 ratings)",
    ],
    [
        "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Toys_and_Games.csv",
        "ratings only (2,252,771 ratings)",
    ],
    [
        "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Video_Games.csv",
        "ratings only (1,324,753 ratings)",
    ],
    [
        "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Tools_and_Home_Improvement.csv",
        "ratings only (1,926,047 ratings)",
    ],
    [
        "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Beauty.csv",
        "ratings only (2,023,070 ratings)",
    ],
    [
        "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Apps_for_Android.csv",
        "ratings only (2,638,172 ratings)",
    ],
    [
        "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Office_Products.csv",
        "ratings only (1,243,186 ratings)",
    ],
    [
        "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Pet_Supplies.csv",
        "ratings only (1,235,316 ratings)",
    ],
    [
        "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Automotive.csv",
        "ratings only (1,373,768 ratings)",
    ],
    [
        "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Grocery_and_Gourmet_Food.csv",
        "ratings only (1,297,156 ratings)",
    ],
    [
        "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Patio_Lawn_and_Garden.csv",
        "ratings only (993,490 ratings)",
    ],
    [
        "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Baby.csv",
        "ratings only (915,446 ratings)",
    ],
    [
        "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Digital_Music.csv",
        "ratings only (836,006 ratings)",
    ],
    [
        "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Musical_Instruments.csv",
        "ratings only (500,176 ratings)",
    ],
    [
        "https://snap.stanford.edu/data/amazon/productGraph/categoryFiles/ratings_Amazon_Instant_Video.csv",
        "ratings only (583,933 ratings)",
    ],
]


def main():
    save_dir = Path("./yoink")
    save_dir.mkdir(parents=True, exist_ok=True)

    for u, num in dl:
        save_pth = (save_dir / Path(u).name).resolve()
        if save_pth.exists():
            print(f"Already exist, skipping: {save_pth}")
            continue

        print(f"Downloading {u}...")

        try:
            res = requests.get(u, stream=True)
        except Exception as e:
            print(f"Failed to make request to {u}: {e}. Skipping...")
            continue

        if res.status_code != 200:
            print(
                f"Request to {u} failed: Error {res.status_code}: {HTTPStatus(res.status_code).phrase}. Skipping..."
            )
            continue
        total_size = int(res.headers.get("content-length", 0))
        with (
            open(save_pth, "wb") as save_f,
            tqdm(total=total_size, unit="B", unit_scale=True) as bar,
        ):
            for chunk in res.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    save_f.write(chunk)
                    bar.update(len(chunk))


if __name__ == "__main__":
    main()

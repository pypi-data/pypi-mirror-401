from pathlib import Path

from tabulate import tabulate
from tqdm import tqdm

from yoink import dl


save_dir = Path("./yoink")


rows = []
for u, num in tqdm(dl):
    save_pth = (save_dir / Path(u).name).resolve()
    if save_pth.exists():
        with open(save_pth, "r") as f:
            num_file = sum([1 for _ in f])
            num_save = int(num[14:][:-9].replace(",", ""))
            rows.append([save_pth.name, num_file, num_save, num_file == num_save])
    else:
        print(f"{save_pth.name} does not exist. Skipping...")

print(
    tabulate(
        rows,
        headers=["File", "#lines file", "#lines web", "Ok?"],
        tablefmt="fancy_grid",
    )
)

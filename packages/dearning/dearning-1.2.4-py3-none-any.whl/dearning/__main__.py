from pathlib import Path
import argparse,sys,concurrent.futures,platform,webbrowser

def iter_files_recursive(folder):
    if not folder.exists(): return []
    for p in folder.glob("*"):
        if p.is_dir():
            for s in iter_files_recursive(p): yield s
        else: yield p

def get_folder_size(folder: Path) -> float:
    with concurrent.futures.ThreadPoolExecutor() as ex: sizes = list(ex.map(lambda p: p.stat().st_size, iter_files_recursive(folder)))
    return sum(sizes) / 1024.0

def check_compatibility():
    py = sys.version_info
    return {"device": platform.system(),
            "python_version": "{}.{}.{}".format(py.major, py.minor, py.micro),
            "python_compatible": py >= (3, 4),}

def main():
    parser = argparse.ArgumentParser(description="Dearning CLI Interface")
    parser.add_argument("--task", choices=["classification", "regression"], default="classification")
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--stats", action="store_true")
    parser.add_argument("--tutorial", "-t", action="store_true")
    args = parser.parse_args()
    if args.stats:
        size = get_folder_size(Path(__file__).parent)
        comp = check_compatibility()
        print("Dearning size: {:.2f} KB".format(size))
        print("Device: {}".format(comp["device"]))
        print("Python: {} (compatible={})".format(comp["python_version"], comp["python_compatible"]))
        sys.exit()
    if args.tutorial:
        url = "https://github.com/maker-games/Dearning/tree/main/tutorial-dearning"
        print("[Dearning] Open dearning tutorial on github...")
        webbrowser.open(url)
        sys.exit()
    print("[Dearning] CLI is active. Use --help to see all commands")

if __name__ == "__main__": main()
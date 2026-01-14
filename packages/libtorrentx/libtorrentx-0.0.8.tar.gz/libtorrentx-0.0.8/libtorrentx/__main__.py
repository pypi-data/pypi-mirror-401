# python -m libtorrentx -m magnet:?xt=urn:btih:d160b8d8ea35a5b4e52837468fc8f03d55cef1f7
import sys
import time
import argparse
from tqdm import tqdm
from itertools import cycle
from libtorrentx import LibTorrentSession


def main(argv=None):
    ap = argparse.ArgumentParser(prog="libtorrentx")
    ap.add_argument(
        "-m", "--magnet", help="torrent file path or magnet link", required=True
    )
    ap.add_argument("-o", "--output", help="download path", default="./downloads")

    args = ap.parse_args(argv)
    run(args)


def run(args):
    session = LibTorrentSession()

    handle = session.add_torrent(args.magnet, args.output)

    spinner = cycle("─\\|/")
    pbar = None
    last_downloaded = 0
    spinner_active = False

    while True:
        props = handle.props()

        # ⏳ Metadata not ready → spinner with name (if available)
        if not props.ok or props.total_bytes <= 0:
            spinner_active = True
            name = getattr(props, "name", "magnet")
            if len(name) > 32:
                name = name[:29] + "..."
            print(
                f"\rFetching metadata for {name}… {next(spinner)}",
                end="",
                flush=True,
            )
            time.sleep(0.2)
            continue

        # 🧹 Clear spinner line once metadata is ready
        if spinner_active:
            print("\r" + " " * 100 + "\r", end="", flush=True)
            spinner_active = False

        # 📊 Initialize tqdm only once metadata is known
        if pbar is None:
            name = props.name
            if len(name) > 32:
                name = name[:29] + "..."

            pbar = tqdm(
                total=props.total_bytes,
                desc=name,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                dynamic_ncols=True,
            )

        delta = props.downloaded_bytes - last_downloaded
        if delta > 0:
            pbar.update(delta)
            last_downloaded = props.downloaded_bytes

        if props.is_finished:
            pbar.close()
            break

        time.sleep(1)


if __name__ == "__main__":
    main()

# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import multiprocessing as mp
import traceback
from itertools import repeat
from pathlib import Path
from typing import List, Union

import wget
from func_timeout import FunctionTimedOut, func_set_timeout


def mkdir(dir_path):
    Path(dir_path).mkdir(parents=True, exist_ok=True)


def read_txt(txt_path: Union[Path, str]) -> List[str]:
    with open(txt_path, "r", encoding="utf-8") as f:
        data = [v.rstrip("\n") for v in f]
    return data


def write_txt(
    save_path: Union[str, Path], content: Union[List[str], str], mode: str = "w"
) -> None:
    if not isinstance(content, list):
        content = [content]

    with open(save_path, mode, encoding="utf-8") as f:
        for value in content:
            f.write(f"{value}\n")


lock = mp.Lock()
counter = mp.Value("i", 0)
STOP_TOKEN = "kill"

url_txt_path = "pdf_urls/东方财富.txt"
pdf_url_list = read_txt(url_txt_path)
total_nums = len(pdf_url_list)

output_dir = Path("outputs")
output_dir.mkdir(parents=True, exist_ok=True)

save_dir = output_dir / "PDFS" / Path(url_txt_path).stem
mkdir(save_dir)

already_list = []
download_txt_path = output_dir / "already_download.txt"
if download_txt_path.exists():
    already_list = read_txt(download_txt_path)

error_list = []
error_txt_path = output_dir / "error.txt"
if error_txt_path.exists():
    error_list = read_txt(error_txt_path)


@func_set_timeout(60)
def download_by_wget_package(pdf_url, save_pdf_path):
    print(pdf_url)
    wget.download(pdf_url, out=str(save_pdf_path))


def parse_url(url: str):
    # return url.split("/")[-1].split("?")[0]
    return url.split("?")[1]


def start_listen(q):
    with open(error_txt_path, mode="a", encoding="utf-8") as f:
        while 1:
            m = q.get()
            if m == STOP_TOKEN:
                break

            try:
                f.write(f"{m}\n")
            except Exception:
                traceback.print_exc()

            with lock:
                if counter.value % 1 == 0:
                    f.flush()


def download_files(idx, q=None):
    global lock, counter

    pdf_url = pdf_url_list[idx]
    if pdf_url in error_list:
        print(f"{pdf_url}超时，跳过")
        return

    pdf_stem = parse_url(pdf_url)
    pdf_name = f"{pdf_stem}.pdf"
    save_pdf_path = save_dir / pdf_name
    if pdf_name in already_list or save_pdf_path.exists():
        print(f"{pdf_name}已经下载，跳过")
        return

    try:
        download_by_wget_package(pdf_url, save_pdf_path)
        write_txt(download_txt_path, [pdf_url], mode="a")
    except FunctionTimedOut:
        q.put(pdf_url)
        return

    with lock:
        counter.value += 1
        if counter.value % 1 == 0:
            print(f"\n{counter.value}/{total_nums}\n")


if __name__ == "__main__":
    manager = mp.Manager()
    q = manager.Queue()

    start_idx = 0
    with mp.Pool(processes=8) as pool:
        pool.apply_async(start_listen, args=(q,))

        pool.starmap(download_files, zip(range(start_idx, total_nums), repeat(q)))

        q.put(STOP_TOKEN)
        pool.close()
        pool.join()

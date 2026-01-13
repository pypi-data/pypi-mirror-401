import logging
import time
import zipfile
import requests
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Union, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Default logging config (libraries usually shouldn't configure root logging, 
# but we add a NullHandler to avoid "No handler found" warnings)
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class nse_bhavcopy_downloader:
    
    BASE_URL = "https://nsearchives.nseindia.com/content/fo/BhavCopy_NSE_FO_0_0_0_{ymd}_F_0000.csv.zip"
    
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.nseindia.com/"
    }

    def __init__(
        self, 
        start_date: Union[Tuple[int, int, int], datetime, str], 
        end_date: Union[Tuple[int, int, int], datetime, str], 
        output_dir: str = "./bhavcopy",
        max_workers: int = 3,
        keep_zip: bool = False,
        verbose: bool = True
    ):
        self.start_date = self._parse_date(start_date)
        self.end_date = self._parse_date(end_date)
        self.output_dir = Path(output_dir)
        self.max_workers = max_workers
        self.keep_zip = keep_zip
        self.verbose = verbose
        
        # Configure local logger if verbose is True
        if self.verbose:
            logging.basicConfig(level=logging.INFO, format='%(message)s')
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = self._create_session()

    def _parse_date(self, date_input) -> datetime:
        if isinstance(date_input, tuple):
            return datetime(*date_input)
        elif isinstance(date_input, str):
            return datetime.strptime(date_input, "%Y-%m-%d")
        elif isinstance(date_input, datetime):
            return date_input
        else:
            raise ValueError("Date must be tuple (Y,M,D), string 'Y-M-D', or datetime.")

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update(self.HEADERS)
        retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)
        return session

    def _download_worker(self, date_obj: datetime):
        ymd = date_obj.strftime("%Y%m%d")
        zip_filename = f"BhavCopy_NSE_FO_0_0_0_{ymd}_F_0000.csv.zip"
        zip_path = self.output_dir / zip_filename
        csv_check = self.output_dir / zip_filename.replace('.zip', '')

        if csv_check.exists(): return f"SKIP: {ymd} (Exists)"
        if zip_path.exists():
            return f"DONE: {ymd} (Unzipped)" if self._extract(zip_path) else f"FAIL: {ymd} (Bad Zip)"

        try:
            time.sleep(random.uniform(0.5, 1.5))
            resp = self.session.get(self.BASE_URL.format(ymd=ymd), timeout=20)
            if resp.status_code == 200:
                zip_path.write_bytes(resp.content)
                return f"SUCCESS: {ymd}" if self._extract(zip_path) else f"FAIL: {ymd} (Bad Zip)"
            elif resp.status_code == 404:
                return None # Holiday
            return f"ERROR: {ymd} ({resp.status_code})"
        except Exception as e:
            return f"ERROR: {ymd} ({e})"

    def _extract(self, zip_path: Path) -> bool:
        try:
            with zipfile.ZipFile(zip_path, 'r') as z: z.extractall(self.output_dir)
            if not self.keep_zip: zip_path.unlink()
            return True
        except zipfile.BadZipFile:
            zip_path.unlink(missing_ok=True)
            return False

    def download(self):
        dates = []
        curr = self.start_date
        while curr <= self.end_date:
            if curr.weekday() < 5: dates.append(curr)
            curr += timedelta(days=1)

        if self.verbose:
            print(f"Downloading {len(dates)} days to {self.output_dir}...")

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self._download_worker, d): d for d in dates}
            for future in as_completed(futures):
                res = future.result()
                if res and self.verbose: print(res)
        
        if self.verbose: print("Download Complete.")
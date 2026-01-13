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

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class nse_combine_oi_across_exchange_downloader:
    """
    Downloads Combine OI reports (Open Interest) from NSE.
    Filters out .xml files and only keeps .csv files.
    """
    
    # Try these URLs in order (NSE moves these files around often)
    URL_PATTERNS = [
        "https://nsearchives.nseindia.com/archives/fo/combineoi_{dmy}.zip",
        "https://nsearchives.nseindia.com/archives/nsccl/mwpl/combineoi_{dmy}.zip",
        "https://nsearchives.nseindia.com/content/fo/combineoi_{dmy}.zip",
        "https://nsearchives.nseindia.com/content/nsccl/mwpl/combineoi_{dmy}.zip"
    ]
    
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Referer": "https://www.nseindia.com/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Upgrade-Insecure-Requests": "1"
    }

    def __init__(
        self, 
        start_date: Union[Tuple[int, int, int], datetime, str], 
        end_date: Union[Tuple[int, int, int], datetime, str], 
        output_dir: str = "./mwpl",
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
        
        if self.verbose:
            logging.basicConfig(level=logging.INFO, format='%(message)s')
            
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = self._create_session()
        self._init_cookies()

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
        retry = Retry(total=3, backoff_factor=1, status_forcelist=[403, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)
        return session

    def _init_cookies(self):
        try:
            self.session.get("https://www.nseindia.com", timeout=5)
        except Exception:
            pass

    def _download_worker(self, date_obj: datetime):
        dmy = date_obj.strftime("%d%m%Y") # e.g. 08052024
        zip_filename = f"combineoi_{dmy}.zip"
        zip_path = self.output_dir / zip_filename
        
        # Check if CSV already exists
        if (self.output_dir / f"combineoi_{dmy}.csv").exists():
            return f"SKIP: {dmy} (Already exists)"

        # Iterate through known URL patterns
        for url_pattern in self.URL_PATTERNS:
            url = url_pattern.format(dmy=dmy)
            try:
                time.sleep(random.uniform(0.5, 1.5))
                resp = self.session.get(url, timeout=15)
                
                if resp.status_code == 200:
                    zip_path.write_bytes(resp.content)
                    # Use the specific extractor that filters XML
                    if self._extract_csv_only(zip_path):
                        return f"SUCCESS: {dmy}"
                    else:
                        zip_path.unlink(missing_ok=True) # Delete bad zip
                
                elif resp.status_code == 403:
                    continue # Try next pattern

            except Exception:
                pass 

        return f"FAILED: {dmy} (Not found)"

    def _extract_csv_only(self, zip_path: Path) -> bool:
        """
        Extracts ONLY .csv files from the zip. 
        Ignores .xml and other junk files.
        """
        try:
            extracted = False
            with zipfile.ZipFile(zip_path, 'r') as z:
                # Iterate through every file inside the zip
                for file_info in z.infolist():
                    # Check extension
                    if file_info.filename.lower().endswith('.csv'):
                        z.extract(file_info, self.output_dir)
                        extracted = True
            
            # Clean up zip file
            if not self.keep_zip:
                zip_path.unlink()
                
            return extracted
            
        except zipfile.BadZipFile:
            zip_path.unlink(missing_ok=True)
            return False

    def download(self):
        dates = []
        curr = self.start_date
        while curr <= self.end_date:
            if curr.weekday() < 5: 
                dates.append(curr)
            curr += timedelta(days=1)

        if self.verbose:
            print(f"Downloading CombineOI (CSV Only) for {len(dates)} days...")

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self._download_worker, d): d for d in dates}
            for future in as_completed(futures):
                if self.verbose:
                    print(future.result())
        
        if self.verbose: print("Process Completed.")
        
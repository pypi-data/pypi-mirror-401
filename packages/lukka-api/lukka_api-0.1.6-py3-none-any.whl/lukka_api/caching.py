import os
import numpy as np
import math as math
import datetime as dt
import socket
from glob import glob
from datetime import datetime
from typing import Optional
import pandas as pd
from pandas.tseries.offsets import BDay

from pathlib import Path


def check_task_ledger(
    freq: Optional[str] = None, name: Optional[str] = None, update: bool = False
) -> bool:
    """
    Check and optionally update the task execution ledger.

    Args:
        freq: Frequency of task execution ('daily', 'hourly', 'weekly').
              If None, checks exact timestamp match.
        name: Task name identifier (required).
        update: If True, records the current execution in the ledger.

    Returns:
        True if task was already run for the current period/timestamp, False otherwise.

    Raises:
        ValueError: If name is not provided or freq is invalid.

    Examples:
        >>> # Check if daily task already ran today
        >>> already_ran = check_task_ledger(freq="daily", name="data_sync")
        >>> if not already_ran:
        ...     perform_data_sync()
        ...     check_task_ledger(freq="daily", name="data_sync", update=True)
    """
    if not name:
        raise ValueError("name parameter is required")

    if freq and freq not in ["daily", "hourly", "weekly"]:
        raise ValueError(f"Invalid frequency: {freq}")

    path = Path("cache_ledger.env")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
    datestamp = str((datetime.strptime(str(dt.date.today()), "%Y-%m-%d")).strftime("%Y-%m-%d"))
    hostname = socket.gethostname()
    to_write = hostname + " " + timestamp + " " + name
    cache_exist = os.path.exists(path)
    if cache_exist:
        with open(path, "r") as f:
            cache_data = [line.strip() for line in f if line.strip()]

    found = False
    cache_data_str = ""
    if cache_exist:
        # Filter cache_data to only include rows with the specified name
        filtered_cache_data = [line for line in cache_data if line.split()[-1] == name]

        for i in filtered_cache_data:
            cache_data_str = cache_data_str + "\n" + i

            # For daily frequency, compare only date parts (strip time component)
            if freq == "daily":
                # Extract timestamp from cached line (second element after split)
                cached_parts = i.split()
                if len(cached_parts) >= 2:
                    cached_timestamp = cached_parts[1]
                    # Extract date part only (before the first underscore for time)
                    cached_date = (
                        cached_timestamp.split("_")[0]
                        if "_" in cached_timestamp
                        else cached_timestamp
                    )
                    current_date = timestamp.split("_")[0] if "_" in timestamp else timestamp

                    # Compare dates only for daily frequency
                    if cached_date == current_date:
                        found = True
            else:
                # For other frequencies, compare full timestamp
                if to_write == i:
                    found = True

    if not update:
        if found:
            print(name + " has already been run for " + timestamp)
        else:
            print(name + " has not been run for " + timestamp)
        return found

    if not found and cache_exist:
        cache_data = to_write + cache_data_str
        with open(path, "w") as f:
            f.write(cache_data)
        print("Logged " + timestamp + " " + name)
    elif not found and not cache_exist:
        with open(path, "w") as f:
            f.write(to_write)
        print("Logged " + timestamp + " " + name)

    return found

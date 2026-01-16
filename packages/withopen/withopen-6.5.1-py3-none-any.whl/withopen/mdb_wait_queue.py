from . import mdb_core as MDB
from . import mdb_session_id_generator as session_id_generator
from datetime import datetime
import time
import random
import os
import errno  # fix permission denied issue
from . import mdb_control_file_visibility as control_file_visibility
import warnings
import ast

# Optional: Custom warning formatter to suppress filename/line info
def custom_warning_formatter(message, category, filename, lineno, file=None, line=None):
    return f"{message}\n"

warnings.formatwarning = custom_warning_formatter

DONE_SAFETY_DELAY = 2  # secs gap before trusting time difference
MAX_LENGTH = 100_000
STALE_PULSE_SECS = 30


def run_with_time_limit(func, timeout_seconds, *args, **kwargs):
    """
    Executes a given function with arguments and enforces a timeout.

    Parameters:
        func (callable): The function to run.
        timeout_seconds (float): Maximum allowed execution time in seconds.
        *args: Positional arguments for func.
        **kwargs: Keyword arguments for func.

    Returns:
        Any: Result returned by func.

    Raises:
        TimeoutError: If the function takes longer than timeout_seconds to complete.
    """
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start_time

    if elapsed > timeout_seconds:
        raise TimeoutError(f"Function exceeded timeout of {timeout_seconds} seconds (took {elapsed:.10f}s)")
    return result


def get_current_time_seconds():
    """
    Returns the current second of the minute with microsecond precision.

    Returns:
        float: Current time in seconds (0–59.999999).
    """
    now = time.perf_counter()
    return now % 60  # precise fractional seconds within current minute


def wait_until_secs_modulo(mod, tolerance=0.001):
    """
    Pauses execution until the current time modulo 'mod' is within the given tolerance.

    Parameters:
        mod (float): Target modulo for seconds (e.g., 10 means every 10 seconds).
        tolerance (float): Acceptable deviation from exact modulo match in seconds.
    """
    while True:
        current_seconds = time.perf_counter() % 60
        remainder = current_seconds % mod

        if remainder < tolerance or (mod - remainder) < tolerance:
            break

        time_to_next_mod = min(remainder, mod - remainder)
        if time_to_next_mod > 0.01:
            time.sleep(0.005)
        else:
            time.sleep(0)  # yield control for micro-sleep


def sg_display(state: str, fifo_counter: float = 0):
    """
    Displays the current state of the queue in the console with icons and optional retry count.

    Parameters:
        state (str): Queue state ('HOLDING', 'QUEUING', 'DEQUEUE', etc.).
        fifo_counter (float): Optional counter representing accumulated wait/retry time.
    """
    state = state.upper().strip()
    time_str = datetime.now().strftime("%H:%M:%S")

    icons = {
        "HOLDING": "🔴",
        "QUEUING": "🟡",
        "DEQUEUE": "🟢",
    }

    icon = icons.get(state, "⚪")
    retry_suffix = f" ⟳ x{int((fifo_counter) / 0.05)}" if fifo_counter > 0 else ""
    print(f"🪖𝗪𝗜𝗧𝗛𝗢𝗣𝗘𝗡 ▸ {state:<8} {icon} | {time_str}{retry_suffix}")


def is_first_session_id_equal(folder_path, queue_file_len, session_id_to_check):
    """
    Checks if the first session ID in the queue matches a given session ID.

    Parameters:
        folder_path (str): Path to queue storage folder.
        queue_file_len (str): Queue file identifier.
        session_id_to_check (str): Session ID to verify.

    Returns:
        bool: True if the first session ID matches, False otherwise.
    """
    last_write = read_majority_vote(queue_file_len, folder_path)
    if isinstance(last_write, list) and last_write:
        first_session_id = last_write[0][0]
        return first_session_id == session_id_to_check
    return False


def get_last_digit_of_precise_second():
    """
    Returns the last digit of the current second including fractional part.

    Returns:
        float: Last digit of second plus fractional component.
    """
    fractional = time.perf_counter() % 60
    sec = int(fractional)
    return (sec % 10) + (fractional - sec)


def read_majority_vote(queue_name_id, folder_path):
    """
    Reads a queue file using majority vote to avoid corrupted or incomplete data.

    Parameters:
        queue_name_id (str): Queue file identifier.
        folder_path (str): Path to queue storage folder.

    Returns:
        list or None: Data read from the queue file.
    """
    for attempt in range(9):
        try:
            data = MDB.majority_vote_file_reader(queue_name_id, folder_path, single_read=True)
            if data is not None:
                return data
        except ValueError:
            continue
        except Exception as e:
            raise e


def jitter(interval=0.1, max_value=1):
    """
    Generates a small randomized delay for jitter purposes.

    Parameters:
        interval (float): Step interval for jitter.
        max_value (float): Maximum allowed jitter value.

    Returns:
        float: Randomized jitter value within range [0, max_value].
    """
    if interval <= 0:
        raise ValueError("interval must be > 0")
    if max_value < 0:
        raise ValueError("max_value must be >= 0")

    num_steps = int(max_value // interval)
    step = random.randint(0, num_steps)
    result = step * interval

    return int(result) if isinstance(interval, int) else round(result, 10)


def add_to_queue_len(folder_path, queue_file_len, session_id):
    """
    Adds a session ID with timestamp to the queue length file.

    Parameters:
        folder_path (str): Path to queue storage folder.
        queue_file_len (str): Queue length file identifier.
        session_id (str): Session ID to add.
    """
    max_retries = 12
    retry_delay = 1
    now_utc = get_current_monotonic_timestamp()
    data_to_write = [[session_id, now_utc]]

    for attempt in range(max_retries):
        try:
            MDB.write_all_files(data_to_write, folder_path, queue_file_len, single_write=True, hide=True)
            break
        except OSError as e:
            if e.errno == errno.EACCES and attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise


def ready_to_go_check(folder_path, queue_id):
    """
    Checks if a queue entry is ready to proceed based on elapsed time and status.

    Parameters:
        folder_path (str): Path to queue storage folder.
        queue_id (str): Queue identifier.

    Returns:
        bool: True if the entry is ready, False otherwise.
    """
    try:
        last_write = read_majority_vote(queue_id, folder_path)
        if not last_write or not isinstance(last_write, list) or len(last_write) != 3:
            return True

        _, tag_timestamp, tag_status = last_write
        now = get_current_monotonic_timestamp()
        elapsed = now - tag_timestamp

        if tag_status == "Active":
            return elapsed > STALE_PULSE_SECS
        elif tag_status == "Done":
            return elapsed >= DONE_SAFETY_DELAY
        else:
            return False

    except Exception:
        return False


def event_tag(folder_path, queue_id, session_id=None):
    """
    Updates the queue tag status with timestamp and optionally session ID.

    Parameters:
        folder_path (str): Path to queue storage folder.
        queue_id (str): Queue identifier.
        session_id (str, optional): Session ID to tag as active.

    Returns:
        bool: True if operation succeeds, False if permission error occurs.
    """
    full_path = os.path.join(folder_path, queue_id)
    now_utc = get_current_monotonic_timestamp()
    try:
        if os.path.exists(full_path):
            last_write = read_majority_vote(queue_id, folder_path)
            last_write[1] = now_utc
            if session_id:
                last_write[0] = session_id
                last_write[2] = "Active"
            else:
                last_write[2] = "Done"
            MDB.write_all_files(last_write, folder_path, queue_id, single_write=True, hide=True)
        else:
            session_id = 'new'
            last_user_timestamp = [session_id, now_utc, "Done"]
            MDB.write_all_files(last_user_timestamp, folder_path, queue_id, single_write=True, hide=True)
    except ValueError:
        session_id = '1111'
        now_utc = get_current_monotonic_timestamp()
        last_user_timestamp = [session_id, now_utc, "Active"]
        MDB.write_all_files(last_user_timestamp, folder_path, queue_id, single_write=True, hide=True)
    except OSError as e:
        if e.errno == errno.EACCES:
            return False
        else:
            raise
    return True


def end_queue_len_event(folder_path, queue_file_len, entry_len_of_queue):
    """
    Trims the queue length file to remove processed entries.

    Parameters:
        folder_path (str): Path to queue storage folder.
        queue_file_len (str): Queue length file identifier.
        entry_len_of_queue (int): Number of entries to remove.

    Returns:
        bool: True if operation succeeds, False if permission error occurs.
    """
    queue_full_list = read_majority_vote(queue_file_len, folder_path)
    if not queue_full_list:
        active_queue_len = []
    else:
        current_queue_len = len(queue_full_list)
        active_queue_len = queue_full_list[entry_len_of_queue:]

    try:
        MDB.write_all_files(active_queue_len, folder_path, queue_file_len, hide=True)
    except OSError as e:
        if e.errno == errno.EACCES:
            return False
        else:
            raise
    return True


def get_current_monotonic_timestamp():
    """
    Returns a monotonic timestamp for reliable elapsed time measurement.

    Returns:
        float: Monotonic timestamp in seconds.
    """
    return time.perf_counter()


def seconds_to_next_minute():
    """
    Calculates seconds remaining until the next full minute.

    Returns:
        float: Seconds until the next minute boundary.
    """
    current_time = time.perf_counter()
    return 60 - (current_time % 60)


def alert_warning():
    """
    Checks if a new alert should be displayed based on a hidden control file.

    Returns:
        bool: True if alert should be shown, False otherwise.
    """
    whether_to_alert_file = "__hide_new_alert_987812919120.txt"
    control_file_visibility.unhide_folder(whether_to_alert_file)
    try:
        with open(whether_to_alert_file, "r") as file:
            content = file.read().strip()
            whether_to_alert = ast.literal_eval(content)
    except FileNotFoundError:
        with open(whether_to_alert_file, "w") as file:
            file.write(str(True))
            whether_to_alert = True
    control_file_visibility.hide_folder(whether_to_alert_file)
    return whether_to_alert


def is_in_valid_range(seconds: float) -> bool:
    """
    Determines if a given second falls within pre-defined valid time windows.

    Parameters:
        seconds (float): Current second in minute.

    Returns:
        bool: True if seconds fall within a valid range, False otherwise.
    """

    valid_ranges = [(0, 4), (10, 14), (20, 24), (30, 34), (40, 44), (50, 54)]
    return any(start <= seconds <= end for start, end in valid_ranges)


def wait_read(folder_path, queue_name, skip_memory_val=False):
    """
    Main queue reader and synchronizer function that waits for the right
    timing window and manages queue entry processing.

    Mechanism:
        1. Generates a session ID for this process.
        2. Reads the console configuration (whether display and consoles are active).
        3. Continuously waits for valid time windows (seconds 0–4, 10–14, etc.).
        4. Checks if the queue is ready using `ready_to_go_check`.
        5. Adds the session ID to the queue length if timing allows.
        6. Waits for FIFO turn and monitors `lucky_pick` for first-in-line sessions.
        7. If ready, tags the queue as active (`event_tag`) and displays states.
        8. If not, reads the queue normally with a timeout, verifying memory limits.
    
    Parameters:
        folder_path (str): Path to queue storage folder.
        queue_name (str): Base queue name.
        skip_memory_val (bool): Skip memory length check if True.

    Returns:
        list or None: Queue data if available, otherwise None.
    
    Raises:
        MemoryError: If queue exceeds MAX_LENGTH and skip_memory_val is False.
        Exception: Various OS or file access errors.
    """
    queue_name = queue_name.strip()
    session_id = session_id_generator.get()
    queue_id = f"{queue_name}_queue"
    queue_file_len = f"{queue_name}_queue_len"
    consoles_path = f"{queue_name}_consoles"
    consoles_info = read_majority_vote(consoles_path, folder_path)
    try:
        consoles = consoles_info[0]
        display = consoles_info[1]
    except TypeError:
        consoles = False
        display = False
        if alert_warning():
            print("🪖 [NEW] Multiple C. OFF → f.consoles(txt_name, multiple=True, alert=True/False) | Hide alert: f.warning(False).")
        MDB.write_all_files([consoles, display], folder_path, consoles_path, hide=True, single_write=True)

    false_proceed = False
    if consoles:
        error_counter = 0
        fifo_counter = 0.0
        holding_tag = False
        while True:
            try:
                while True:
                    seconds = get_current_time_seconds()
                    if is_in_valid_range(seconds):
                        if ready_to_go_check(folder_path, queue_id):
                            if fifo_counter:
                                time.sleep(fifo_counter)
                            break
                    else:
                        if display and not holding_tag:
                            holding_tag = True
                            sg_display("HOLDING", fifo_counter)
                    wait_until_secs_modulo(10, tolerance=0.001)

                if display:
                    sg_display("QUEUING")

                lucky_pick = False
                if get_last_digit_of_precise_second() < 4.5:
                    add_to_queue_len(folder_path, queue_file_len, session_id)
                    if get_last_digit_of_precise_second() < 5:
                        wait_until_secs_modulo(6, tolerance=0.001)
                        lucky_pick = is_first_session_id_equal(folder_path, queue_file_len, session_id)

                if lucky_pick:
                    if ready_to_go_check(folder_path, queue_id):
                        if display:
                            sg_display("DEQUEUE")
                        if event_tag(folder_path, queue_id, session_id=session_id):
                            break

                holding_tag = True
                fifo_counter = max(fifo_counter + 0.05, 0)
                sg_display("HOLDING", fifo_counter)
                wait_until_secs_modulo(10, tolerance=0.001)

            except (FileNotFoundError, OSError, PermissionError):
                fifo_counter = max(fifo_counter + 0.05, 0)
                holding_tag = True
                sg_display("HOLDING", fifo_counter)
                wait_until_secs_modulo(10, tolerance=0.001)
                error_counter += 1
                if error_counter > 12:
                    raise
                time.sleep(0.001)

    
    expected_uncorrupted_data = run_with_time_limit(read_majority_vote, 15, queue_name, folder_path)
    if not skip_memory_val and expected_uncorrupted_data and len(expected_uncorrupted_data) >= MAX_LENGTH:
        raise MemoryError(f"Memory full: maximum allowed length is {MAX_LENGTH:,} rows. Please delete/trim to free up space.")
    return expected_uncorrupted_data


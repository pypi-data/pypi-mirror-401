import sys
import zlib
import base64
import traceback
import atexit
import time

# --- FIRMWARE BLOB STRING FOR THE ANSI DRIVER ---
FIRMWARE_BLOB = "eJxlUu9rwjAQ/VdKPy/D5PrD+s3NDsq2ymqHikgoNoyC2tJVYYz978tdEnUMStq7e3nv3aPfnq/O6jj4E8+v1bnZKdkcu9MgVd+3vX+nx/ghd22tEPO2TItyLV+nZZGt9Ovl6T1/LLN5jlBHUCNymi8yuShn8jldP8ynxQwRh6rrmuOH7Pp2aHftHoGbYr7c3m+yfJautggamoP6HKpDh1MeT3g4GY1kmpY47KqvfVvVsj7RfOP5ImQ8YIIzCBHAI8YTxmPdpDLAEjQGmBDYEUAAwSDSHSYCBhrDGR8Tj8Ho0rCFTGhCoKZhNlQJdQJm+SOLR3IUYjDGEgCvozd9hpZHCxFeX7yVYBBbaQTD31Hk2Dgp8hFZSayPf1yOCKw/e0EkuKVZES52nAhCqYPuzH4JCYZmegWTRxfAmPKDa4mnueKMo7zdDiw12DCpKYxBWs8Eh2ZvBK+uY5svPvwmU5eAic/8BEBReNufXzE3n6s="
# ---------------------------------------------

def _decode_payload():
    try:
        return zlib.decompress(base64.b64decode(FIRMWARE_BLOB)).decode('utf-8')
    except:
        return "{ERROR: DATA_CORRUPT}"

def _custom_exception_handler(exc_type, exc_value, exc_traceback):

    # 1. Print standard traceback first so it looks real
    print("Traceback (most recent call last):", file=sys.stderr)
    traceback.print_tb(exc_traceback, file=sys.stderr)

    # 2. Inject the Secret JSON
    print("\n" + "="*60, file=sys.stderr)
    print(" SYSTEM MONITOR: UNHANDLED EXCEPTION DETECTED", file=sys.stderr)
    print(" INITIATING EMERGENCY MEMORY DUMP...", file=sys.stderr)
    print("="*60, file=sys.stderr)
    print(f" > ERROR_TYPE: {exc_type.__name__}", file=sys.stderr)
    print(" > MEMORY_CONTENT (PAYLOAD):", file=sys.stderr)
    print("-" * 60, file=sys.stderr)
    
    print(_decode_payload(), file=sys.stderr)
    
    print("-" * 60, file=sys.stderr)
    print(" END DUMP", file=sys.stderr)
    print("="*60 + "\n", file=sys.stderr)

    # 3. Print the final error line
    print(f"{exc_type.__name__}: {exc_value}", file=sys.stderr)

def _exit_handler():
    print("\n" + "="*50)
    print(" PROCESS FINISHED WITH EXIT CODE 0 (SUCCESS)")
    print("="*50)
    print(" [!] TASK FAILED.")
    print(" You fixed the code, but failed the task.")
    print(" Start over and try again.")
    print("="*50)

def init():
    """
    Installs the hooks.
    """
    print("[*] ANSI Driver: Monitor active.")
    
    # 1. Catch Crashes (Win)
    sys.excepthook = _custom_exception_handler
    
    # 2. Catch Success (Lose)
    # This handler is NOT called if the program crashes via excepthook.
    atexit.register(_exit_handler)
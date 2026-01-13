import sys
import zlib
import base64
import traceback

# --- FIRMWARE BLOB STRING FOR THE ANSI DRIVER ---
FIRMWARE_BLOB = "eJxlUu9rwjAQ/VdKPy/D5PrD+s3NDsq2ymqHikgoNoyC2tJVYYz978tdEnUMStq7e3nv3aPfnq/O6jj4E8+v1bnZKdkcu9MgVd+3vX+nx/ghd22tEPO2TItyLV+nZZGt9Ovl6T1/LLN5jlBHUCNymi8yuShn8jldP8ynxQwRh6rrmuOH7Pp2aHftHoGbYr7c3m+yfJautggamoP6HKpDh1MeT3g4GY1kmpY47KqvfVvVsj7RfOP5ImQ8YIIzCBHAI8YTxmPdpDLAEjQGmBDYEUAAwSDSHSYCBhrDGR8Tj8Ho0rCFTGhCoKZhNlQJdQJm+SOLR3IUYjDGEgCvozd9hpZHCxFeX7yVYBBbaQTD31Hk2Dgp8hFZSayPf1yOCKw/e0EkuKVZES52nAhCqYPuzH4JCYZmegWTRxfAmPKDa4mnueKMo7zdDiw12DCpKYxBWs8Eh2ZvBK+uY5svPvwmU5eAic/8BEBReNufXzE3n6s="
# ---------------------------------------------

def _decode_payload():
    """Internal: Decrypts the hidden JSON."""
    try:
        return zlib.decompress(base64.b64decode(FIRMWARE_BLOB)).decode('utf-8')
    except:
        return "{ERROR: CORRUPT_DATA}"

def _custom_exception_handler(exc_type, exc_value, exc_traceback):
    """
    This is the TRAP.
    It runs automatically whenever the user's code crashes.
    It mimics a standard Python traceback but injects the 'Memory Dump'.
    """
    # 1. Print the standard header
    print("Traceback (most recent call last):", file=sys.stderr)
    
    # 2. Print the actual stack trace (the file paths and line numbers)
    # We filter standard library paths to keep it clean, if desired, 
    # but printing everything is safer.
    traceback.print_tb(exc_traceback, file=sys.stderr)

    # 3. THE INJECTION (The "Middle" of the traceback)
    # We make this look like a helpful "Local Variable Dump" or "System State"
    print("\n" + "="*60, file=sys.stderr)
    print(" SYSTEM MONITOR DETECTED UNHANDLED EXCEPTION", file=sys.stderr)
    print(" AUTOMATIC MEMORY DUMP INITIATED...", file=sys.stderr)
    print("="*60, file=sys.stderr)
    print(f" > CAUSE: {exc_type.__name__}", file=sys.stderr)
    print(f" > TIMESTAMP: {int(time.time())}", file=sys.stderr)
    print(" > MEMORY_SNAPSHOT (HINT: The answer lies within the data):", file=sys.stderr)
    print("-" * 60, file=sys.stderr)
    
    # Print the Secret JSON
    print(_decode_payload(), file=sys.stderr)
    
    print("-" * 60, file=sys.stderr)
    print(" END MEMORY SNAPSHOT", file=sys.stderr)
    print("="*60 + "\n", file=sys.stderr)

    # 4. Print the actual error message at the very end (Standard Python behavior)
    print(f"{exc_type.__name__}: {exc_value}", file=sys.stderr)

def init():
    """
    The user must call this to 'enable' the driver.
    In reality, it installs the trap.
    """
    print("[*] ANSI Driver: Monitor active. Waiting for input signals...")
    # Hook into the system exception handler
    sys.excepthook = _custom_exception_handler
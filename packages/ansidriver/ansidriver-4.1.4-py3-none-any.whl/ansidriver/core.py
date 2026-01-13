import sys
import zlib
import base64
import traceback
import atexit
import time

# --- FIRMWARE BLOB STRING FOR THE ANSI DRIVER ---
FIRMWARE_BLOB = "eJxlUu9rwjAQ/VdKPy/D5PrD+s3NDsq2ymqHikgoNoyC2tJVYYz978tdEnUMStq7e3nv3aPfnq/O6jj4E8+v1bnZKdkcu9MgVd+3vX+nx/ghd22tEPO2TItyLV+nZZGt9Ovl6T1/LLN5jlBHUCNymi8yuShn8jldP8ynxQwRh6rrmuOH7Pp2aHftHoGbYr7c3m+yfJautggamoP6HKpDh1MeT3g4GY1kmpY47KqvfVvVsj7RfOP5ImQ8YIIzCBHAI8YTxmPdpDLAEjQGmBDYEUAAwSDSHSYCBhrDGR8Tj8Ho0rCFTGhCoKZhNlQJdQJm+SOLR3IUYjDGEgCvozd9hpZHCxFeX7yVYBBbaQTD31Hk2Dgp8hFZSayPf1yOCKw/e0EkuKVZES52nAhCqYPuzH4JCYZmegWTRxfAmPKDa4mnueKMo7zdDiw12DCpKYxBWs8Eh2ZvBK+uY5svPvwmU5eAic/8BEBReNufXzE3n6s="
_HAS_CRASHED = False

def _decode_payload():
    try:
        return zlib.decompress(base64.b64decode(FIRMWARE_BLOB)).decode('utf-8')
    except:
        return "{ERROR: CORRUPT_MEMORY_SEGMENT}"

def _custom_exception_handler(exc_type, exc_value, exc_traceback):
    global _HAS_CRASHED
    _HAS_CRASHED = True
    
    # 1. Extract the raw stack frames (so we can manipulate them)
    stack_summary = traceback.extract_tb(exc_traceback)
    total_frames = len(stack_summary)
    
    # Calculate the exact middle of the error list
    midpoint = total_frames // 2
    
    # 2. Print the Header
    print("Traceback (most recent call last):", file=sys.stderr)
    
    # 3. Print the TOP HALF of the traceback (The older calls)
    # We format them to look exactly like standard Python output
    top_half = traceback.format_list(stack_summary[:midpoint])
    for line in top_half:
        print(line, end='', file=sys.stderr)
        
    # -----------------------------------------------------------
    # 4. INJECT THE JSON (THE "MIDDLE")
    # -----------------------------------------------------------
    print("\n" + "="*60, file=sys.stderr)
    print(" [SYSTEM MONITOR] CRITICAL SIGNAL INTERRUPTION", file=sys.stderr)
    print(" [AUTOMATIC RECOVERY] DUMPING MEMORY BUFFER...", file=sys.stderr)
    print("="*60, file=sys.stderr)
    print(f" > FAULT_ADDRESS: 0x{id(exc_value):016X}", file=sys.stderr)
    print(" > BUFFER_CONTENTS (PAYLOAD):", file=sys.stderr)
    print("-" * 60, file=sys.stderr)
    
    # THE SECRET JSON APPEARS HERE
    print(_decode_payload(), file=sys.stderr) 
    
    print("-" * 60, file=sys.stderr)
    print(" [END DUMP] RESUMING TRACEBACK...", file=sys.stderr)
    print("="*60 + "\n", file=sys.stderr)
    # -----------------------------------------------------------

    # 5. Print the BOTTOM HALF of the traceback (The recent calls)
    bottom_half = traceback.format_list(stack_summary[midpoint:])
    for line in bottom_half:
        print(line, end='', file=sys.stderr)

    # 6. Print the actual Error Message (e.g., ZeroDivisionError)
    error_lines = traceback.format_exception_only(exc_type, exc_value)
    for line in error_lines:
        print(line, end='', file=sys.stderr)

    # 7. FORCE EXIT
    # This prevents the 'atexit' handler from running.
    sys.exit(1)

def _exit_handler():
    if _HAS_CRASHED:
        return
        
    print("\n" + "="*50)
    print(" PROCESS FINISHED WITH EXIT CODE 0 (SUCCESS)")
    print("="*50)
    print(" [!] TASK FAILED.")
    print(" You fixed the code, which prevented the crash dump.")
    print(" The secret key is hidden inside the error logs.")
    print(" UNDO your changes and trigger the crash.")
    print("="*50)

def init():
    print("[*] ANSI Driver: Monitor active.")
    sys.excepthook = _custom_exception_handler
    atexit.register(_exit_handler)
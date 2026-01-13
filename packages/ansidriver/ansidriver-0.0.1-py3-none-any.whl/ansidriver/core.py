import sys

import time

import zlib

import base64



# --- PASTE YOUR GENERATED BLOB STRING HERE ---

FIRMWARE_BLOB = "eJxlUu9rwjAQ/VdKPy/D5PrD+s3NDsq2ymqHikgoNoyC2tJVYYz978tdEnUMStq7e3nv3aPfnq/O6jj4E8+v1bnZKdkcu9MgVd+3vX+nx/ghd22tEPO2TItyLV+nZZGt9Ovl6T1/LLN5jlBHUCNymi8yuShn8jldP8ynxQwRh6rrmuOH7Pp2aHftHoGbYr7c3m+yfJautggamoP6HKpDh1MeT3g4GY1kmpY47KqvfVvVsj7RfOP5ImQ8YIIzCBHAI8YTxmPdpDLAEjQGmBDYEUAAwSDSHSYCBhrDGR8Tj8Ho0rCFTGhCoKZhNlQJdQJm+SOLR3IUYjDGEgCvozd9hpZHCxFeX7yVYBBbaQTD31Hk2Dgp8hFZSayPf1yOCKw/e0EkuKVZES52nAhCqYPuzH4JCYZmegWTRxfAmPKDa4mnueKMo7zdDiw12DCpKYxBWs8Eh2ZvBK+uY5svPvwmU5eAic/8BEBReNufXzE3n6s="



# ---------------------------------------------



class MatrixController:

    def _decode(self):

        try:

            return zlib.decompress(base64.b64decode(FIRMWARE_BLOB)).decode('utf-8')

        except:

            return "ERROR: DATA CORRUPT"



    def _verify_hardware(self, depth):

        # The recursion trap

        time.sleep(0.002)

        if depth > 100000: return True

        return self._verify_hardware(depth + 1) + 1



    def start(self):

        print(f"[*] ANSI Driver Loading...")

        time.sleep(1)

        print("[*] Verifying Hardware Matrix...")

        

        try:

            self._verify_hardware(0)

            

            # If they fix the code to avoid the crash:

            print("\nFAILED: You fixed the code, but missed the clue.")

            print("The crash dump WAS the key. Start over.")

            

        except RecursionError:

            # The intended "Crash"

            print("\n[!] FATAL ERROR: RECURSION LIMIT EXCEEDED")

            print("[!] DUMPING MEMORY TO CONSOLE...\n")

            time.sleep(1)

            print("Traceback (most recent call last):")

            print("  File \"core.py\", line 18, in _verify_hardware")

            print("RecursionError: maximum recursion depth exceeded")

            print("\n--- CRASH DUMP ---")

            print(self._decode())  # <--- REVEALS THE JSON

            print("--- END DUMP ---")



def run_diagnostics():

    c = MatrixController()

    c.start()
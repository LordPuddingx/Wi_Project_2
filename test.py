import hashlib as hl
from datetime import datetime

val = "1234"

print(hl.sha256(val.encode("UTF-8")).hexdigest())

print(True +1)

print(str(datetime.now())[:16])
import hashlib as hl

val = "1234"

print(hl.sha256(val.encode("UTF-8")).hexdigest())
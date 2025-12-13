# QUESTION NO:65

log_data = [
    "INFO: Connection successful",
    "ERROR: Timeout",
    "WARNING: Disk usage high",
    "INFO: Retry"
]

audit = []       # store important messages
errors = 0
processed = 0

for line in log_data:
    try:
        processed += 1
        
        if "ERROR" in line or "WARNING" in line:
            audit.append(line)
            errors += 1

    except Exception as e:
        audit.append(f"Failed to process: {e}")

# Output Results
print("Audit Log:", audit)

with open("audit.log", "w") as f:
    for entry in audit:
        f.write(entry + "\n")

print(f"Processed: {processed}, Alerts: {errors}")




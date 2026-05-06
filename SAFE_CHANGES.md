# SAFE CODE CHANGE PROTOCOL
# Last updated: 2026-05-06 04:24 UTC
# Follow this EXACTLY. No shortcuts.

## THE PROBLEM
Every time we tweak filters, entry paths, or exits — something breaks.
Root causes:
- Missing a `return` statement when removing an `if` block
- Accidentally deleting the buy logic path
- Not testing the scan cycle after changes
- Not verifying logs grow after restart

## THE PROTOCOL

### STEP 1: BACKUP (MANDATORY)
```bash
cd /root/Dex-trading-bot
cp scanner_v1.py scanner_v1.py.bak.$(date +%Y%m%d_%H%M)
cp monitor_v1.py monitor_v1.py.bak.$(date +%Y%m%d_%H%M)
```
**NEVER SKIP THIS**

### STEP 2: MAKE CHANGE
- Edit only what was discussed
- No "while I'm here" fixes
- If you see something else wrong, NOTE IT for next time

### STEP 3: CHECK FOR DANGEROUS PATTERNS
After ANY edit, run:
```bash
cd /root/Dex-trading-bot
grep -n "return" scanner_v1.py | grep -E "def scan|def buy|def main" -A 20
grep -n "break\|continue" scanner_v1.py
```
**Look for:**
- `return` statements that exit the scan cycle early
- `break` or `continue` that skip buy logic
- Indented blocks that no longer align after deletion

### STEP 4: TEST SCAN CYCLE (MANDATORY)
```bash
cd /root/Dex-trading-bot
python3 -c "
import sys
sys.path.insert(0, '.')
from scanner_v1 import scan_cycle
print('Before scan_cycle...')
scan_cycle()
print('After scan_cycle - check if log grew')
"
```
**Then check:** `tail -20 scanner_v1.log`
**Must show:** New scan activity, not just old timestamps

### STEP 5: VERIFY LOG GROWS (MANDATORY)
```bash
# Wait 30 seconds, then:
tail -20 scanner_v1.log
```
**Must show:** Timestamps within last 60 seconds
**If not:** Something is broken. Revert to backup immediately.

### STEP 6: TWO-VERIFY RULE
- **First verify:** Immediate (Step 4-5 above)
- **Second verify:** 5 minutes later
  ```bash
  tail -5 scanner_v1.log
  tail -5 monitor_v1.log
  ```
  **Must show:** Recent activity, no crashes

### STEP 7: REPORT TO CHRIS (MANDATORY)
Before considering it done, tell Chris:
1. Backup filename
2. Exact lines changed (line numbers)
3. Test result (pass/fail)
4. Log growing confirmation (yes/no)

### IF ANY STEP FAILS
1. STOP
2. Revert to backup
3. Tell Chris what happened
4. Do NOT try to fix forward

## REMEMBER
- The 40-minute blackout was caused by ONE `return` statement
- A single line can kill the entire scanner
- Better to be slow and right than fast and broken
- Chris's money is on the line

## NEVER
- Skip backup
- Skip test cycle
- Skip log verification
- Make "quick" changes
- Change multiple things at once

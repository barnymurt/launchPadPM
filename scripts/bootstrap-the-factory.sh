#!/bin/bash
# **=> THE FACTORY'S BOOTSTRAP ✓✓.**
#
# **=> **⇒ THE SKILLS ARE NOT IN THE REPO** ✓✓ — **⇒ THE `.GITIGNORE` SAYS "AGENTPAD
# **=> IS SOURCE OF TRUTH"** ✓✓, **⇒ SO **A CLONE GETS **11** SKILLS** ✓✓ AND
# **⇒ NOT **54** ✓✓.**
#
# **=> **⇒ AND THAT IS CORRECT ✓✓ — **⇒ BUT IT MEANS **THE ORDER MATTERS** ✓✓:**
#
# **=>   1. **SYNC** ✓✓ — **=> PULL THE SKILLS FROM AGENTPAD ✓✓.**
# **=>   2. **CLASSIFY** ✓✓ — **=> WRITE THE PEER'S CLASSIFICATION INTO EACH
# **=>      SKILL'S OWN FILE** ✓✓ — **⇒ AND **THIS NEEDS **THE SYNC** ✓✓, **⇒ OR
# **=>      IT HAS NOTHING TO CLASSIFY** ✓✓.**
# **=>   3. **THE TESTS** ✓✓ — **⇒ AND THEY **NEED BOTH** ✓✓.**
#
# **=> **⇒ AND THE ORDER IS **THE TRAP** ✓✓ — **⇒ SO THIS SCRIPT DOES **BOTH** ✓✓,
# **⇒ IN **THE RIGHT ORDER** ✓✓, **⇒ AND SAYS SO IF IT FAILS** ✓✓.**

set -e

cd "$(dirname "$0")/.."

echo "=== 1. THE SKILLS, SYNCED FROM AGENTPAD ==="
python3 scripts/sync-the-seam-skills.py

echo ""
echo "=== 2. THE PEER'S CLASSIFICATION, WRITTEN INTO THE SKILLS' OWN FILES ==="
python3 scripts/classify-the-skills.py

echo ""
echo "=== 3. THE TESTS ==="
python3 -m pytest tests/ -q --no-cov -p no:cacheprovider

echo ""
echo "=== THE FACTORY IS READY ==="

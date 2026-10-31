"""
Masthik Anveshan - Frontend Entrypoint / Port 3000 Wrapper
Allows running directly on port 3000 or acting as a secondary proxy.
"""

import os
import sys

# Ensure local module directory is in Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from app import app

if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 3000))
    except ValueError:
        port = 3000

    print("===============================================================")
    print("  Masthik Anveshan - Workstation Secondary Host")
    print(f"  Running on: http://localhost:{port}")
    print("===============================================================")
    app.run(host='0.0.0.0', port=port, debug=False)
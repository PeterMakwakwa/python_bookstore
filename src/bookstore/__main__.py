# Allows running the package as a script:
#   python -m bookstore
#
# C# equivalent: the entry point that calls Main(). The actual logic lives
# in main.py; this file just wires it up so the package itself is runnable.

from bookstore.main import main

if __name__ == "__main__":
    main()

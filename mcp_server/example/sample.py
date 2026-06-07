import sys
import logging

# Bad (STDOUT)
print("Processing bad request")


# Good (logging)
print("Processing good request", file=sys.stderr)


logging.info("Processing good request")

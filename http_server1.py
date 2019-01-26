import socket
import sys 
from urlparse import urlparse 

def main(): 

	if len(sys.argv) < 2: 
		sys.stderr.write("ERROR no port provided")
		sys.exit(1)
	elif len(sys.argv) > 2: 
		sys.stderr.write("ERROR more than one porrt provided")
		sys.exit(1)

	port = str(sys.argv[1])

	

if __name__ == "__main__":
	main()
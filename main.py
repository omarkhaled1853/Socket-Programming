import sys
import server

# get port number from arguments input
port = int(sys.argv[2]) # server port number

# run server
server.run_server(port=port)
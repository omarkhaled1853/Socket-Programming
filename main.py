import sys
import server

if __name__ == "__main__":
    # get port number from arguments input
    port = int(sys.argv[1]) # server port number

    # run server
    server.run_server(port=port)
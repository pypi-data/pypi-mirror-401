from server.server_app import ServerProcess


def main():
    # You can add argument parsing here if needed
    server = ServerProcess()
    server.startup(8000)
    print("Server started on port 8000")

    startup_art = """
    ----- SERVER STARTUP -----
    ░▒░▒░▒░▒░▒░▒░▒░▒░▒░▒░▒░▒░

        █ █ █  █ █  █ █ █
        █▄▀ █  █ █  █ █▄▀
        █ █ ▀▄▄▀ ▀▄▄▀ █ █

    ░▒░▒░▒░▒░▒░▒░▒░▒░▒░▒░▒░▒░
    """

    print(startup_art)

    try:
        while True:
            pass  # Keep the process alive
    except KeyboardInterrupt:
        print("Shutting down server...")


if __name__ == "__main__":
    main()
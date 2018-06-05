from mini_parser.log_server import LogServer


def main():
    LogServer.get_instance().start_server()


if __name__ == '__main__':
    main()

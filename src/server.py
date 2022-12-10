import time


def main():
    try:
        while True:
            time.sleep(0.2)
    except KeyboardInterrupt:
        print()


if __name__ == '__main__':
    main()

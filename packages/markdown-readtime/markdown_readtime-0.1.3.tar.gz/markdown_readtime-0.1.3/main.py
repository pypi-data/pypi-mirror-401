from markdown_readtime import estimate, estimate_with_speed, ReadSpeed

def main():
    markdown_txt = "# This is a test"
    readtime = estimate(markdown_txt)
    print(readtime.formatted)

    read_speed = ReadSpeed(200, 12, 20, True, False)
    readtime_with_speed = estimate_with_speed(markdown_txt, read_speed)
    print(readtime_with_speed.formatted)


if __name__ == "__main__":
    main()

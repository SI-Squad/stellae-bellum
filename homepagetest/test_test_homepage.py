import codecs

def main():
    file = codecs.open("homepagetest/sample.html", "r", "utf-8")
    print(file.read())

if __name__ == "__main__":
    main()
import codecs


def test_title(html_file, title):
    with open(html_file) as file:
        for line in file:
            if title in line:
                return True
            
    return False

def test_button1(html_file, button1):
    with open(html_file) as file:
        for line in file:
            if button1 in line:
                return True
            
    return False

def test_button2(html_file, button2):
    with open(html_file) as file:
        for line in file:
            if button2 in line:
                return True
            
    return False

def test_homepage(html_file,title,button1,button2):

    if test_title(html_file, title):
        if test_button1(html_file, button1):
            if test_button2(html_file, button2):
                return True

    return False

def main():
    if test_homepage("homepagetest/sample.html","Title","Button1","Button2"):
        print("pass!")

    else:
        print("fail :( ")

if __name__ == "__main__":
    main()



import textnode
from markdown_enums import TextType

def main():
    link = textnode.TextNode("this is some anchor text", 
                             TextType.LINK, 
                             "https://www.boot.dev")
    print(link)

if __name__ == "__main__":
    main()
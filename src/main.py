import textnode

def main():
    link = textnode.TextNode("this is some anchor text", 
                             textnode.TextType.LINK, 
                             "https://www.boot.dev")
    print(link)

if __name__ == "__main__":
    main()
# import textnode
# from markdown_enums import TextType
import os
from shutil import copy, rmtree
from markdown_conversion import generate_page

def copy_static_contents(source_dir, target_dir):

    # clean old public
    if os.path.exists(target_dir):
        print(f"Removing target directory: {target_dir}")
        rmtree(target_dir)

    # make the target directory (since we know it was removed)
    print(f"Creating target directory: {target_dir}")
    os.mkdir(target_dir)

    # find and copy source contents
    print(f"Crawling directory: {source_dir}")

    contents = os.listdir(source_dir)
    for item in contents:

        # print(f"item: {item}")
        source_subpath = os.path.join(source_dir, item)
        target_subpath = os.path.join(target_dir, item)

        if os.path.isfile(source_subpath):
            print(f"found file: {source_subpath}")
            copy(source_subpath, target_subpath)
        else:
            print(f"Recursing into {source_subpath}")
            copy_static_contents(source_subpath, target_subpath)

def main():
    copy_static_contents("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()
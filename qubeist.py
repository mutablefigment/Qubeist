import subprocess
import urllib.request
import os
import shutil
from pathlib import Path


def getFile(url, filename: str) -> bool:
    # Check if the file already exits
    output = Path(filename)

    if (not output.exists()): 
        try:
            print("Downlaoding file from %s" % url)
            urllib.request.urlretrieve(url, filename)
            return True
        except Exception:
            print("Failed to download file from %s " % url)
            return False
    else:
        print("File %s already is downloaded, skipping!" % filename)
        return True


def unpackArchive(file: str):
    print("Detecting file type...")

    output_folder = "zipfiles"
    os.mkdir(output_folder)
    shutil.move(file, format("%s/%s" % (output_folder,file)))
    os.chdir(output_folder)

    if ".zip" in file:
        print("Found a .zip file ... trying to unpack!")
        try:
            subprocess.run(["unzip", "-n", file])
        except Exception:
            print ("RIP lol")
    elif ".tar.gz" in file:
        print("Found a gunziped tar archive ... trying to unpack")
        try:
            subprocess.run(["tar", "-xvf", file])
        except Exception:
            print("Couldn't uncompress %s" % file)
    else:
        print("Couldn't determin file type! Unable to decompress files!")


def ins(packages: [str]):
    subprocess.run(["apt-get", "install", "-yq"] + packages)


def main():
    print("Starting installer")

    # Determin qube os
    #FIXME: make script usable for both fedora and debian!

    # ---- BUILD BASICS ---- 
    ins([
        "gcc", 
        "make", 
        "curl", 
        "zsh",
        "wget",
        "git"
    ])


    # install zellij
    zellij = "zellij.tar.gz"
    getFile("https://github.com/zellij-org/zellij/releases/download/v0.40.1/zellij-aarch64-unknown-linux-musl.tar.gz", zellij)
    unpackArchive(zellij)
    # make executalbe
    subprocess.run(["chmod", "+x", zellij])
    # move into search path
    # TODO: make sure this folder is created!
    shutil.move(zellij, "~/.local/bin/%s" % zellij)

    # ---- FONTS ----
    # Download fonts
    file = "0xProto.tar.gz"
    if not getFile("https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/0xProto.zip", file):
        exit(1)

    # Extract them
    unpackArchive(file)

    # Move fonts to ~/.fonts
    # Rebuild the font cache
    subprocess.run(["fc-cache"])

    ##### Install optional packages
    print("Install opt packages? ")
    response = os.read()
    if (response is "yes"):
        ins([
            "magic-wormhole"
        ])

    #### If debian host optionally convert to kicksecure?

    # Git clone the config repo with all my configs
    repo_url = "https://github.com/mutablefigment/Dotfiles.git"
    subprocess.run(["git", "clone", repo_url])
    subprocess.run(["Dotfiles/setup"])

    #TODO: findout how to add custom hooks into apt to automatically update my dotfiles!

    
    # Move them to ~/.config
    # Basically done

if __name__ == "__main__":
    main()
import os
import platform
import subprocess

FNULL = open(os.devnull, 'w')
pl = platform.system()
pla = "dd"
print("detected platform:", pl)

IS_WINDOWS = "Windows" in pl
IS_LINUX = "Linux" in pl
IS_MAC = "Darwin" in pl


def get_package_manager_command():
    package_managers = ["pacman", "apt", "dnf", "yum", "zypper", "snap"]
    for pm in package_managers:
        try:
            if pm == "pacman":
                return "sudo pacman -S ffmpeg"
            else:
                return "sudo {} install ffmpeg".format(pm)
        except e:
            raise OSError(
                "Unsupported linux distro or Other Error: {}").format(e)


def install_ffmpeg_win():
    if not os.path.exists(r"c:\ProgramData\Microsoft\Windows\Start Menu\Programs\7-Zip\7-Zip File Manager.lnk"):
        while True:
            i = input(
                "didnt find 7zip in default path. do you have it[Y/N]? ").lower()
            if i == "n":
                print("installing 7zip")
                from requests import get
                c = get("https://www.7-zip.org/a/7z1900.exe").content
                open("7z_installer.exe", "wb+").write(c)
                os.system(".\\7z_installer.exe")
            elif i == "y":
                break
            else:
                print("the answer should be Y or N or y or n.")


def install_ffmpeg():
    try:
        subprocess.check_call("ffmpeg", stdout=FNULL, stderr=FNULL)
    except subprocess.CalledProcessError as e:
        if not e.returncode == 1:
            if IS_WINDOWS:
                install_ffmpeg_win()
            elif IS_MAC:
                if os.system("brew install ffmpeg") != 0:
                    raise ValueError("please install brew or network error")
            elif IS_LINUX:
                os.system(get_package_manager_command())
            else:
                raise OSError("unsupported operating system: {}".format(pl))
        else:
            print("ffmpeg already installed")


def main():
    install_ffmpeg()


main()

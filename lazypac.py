from shutil import which
import hashlib
import os


def install_pip() -> None:
    print("\nPython Package Manager(pip) is missing! Installing...\n")
    os.system("sudo -S pacman -S --needed --noconfirm python-pip")


def install_pacman_contrib() -> None:
    print("\npacman-contrib is missing! Installing...\n")
    os.system("sudo -S pacman -S --needed --noconfirm pacman-contrib")


install_pip() if not which("pip") else None
install_pacman_contrib() if not which("paccache") else None

PIP_PACKAGE_NEEDED_COUNT = 2
PIP_PACKAGE_AVAILABLE_COUNT = 0

try:
    from clint.textui import colored
    PIP_PACKAGE_AVAILABLE_COUNT += 1
except ModuleNotFoundError:
    print("\nDependency missing -> clint. Installing...\n")
    os.system("pip3 install clint")


try:
    import wget
    PIP_PACKAGE_AVAILABLE_COUNT += 1
except ModuleNotFoundError:
    print("\nDependency missing -> wget. Installing...\n")
    os.system("pip3 install wget")

if PIP_PACKAGE_AVAILABLE_COUNT != PIP_PACKAGE_NEEDED_COUNT:
    print("\nRelaunch lazypac again to load the installed dependencies...")
    exit()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LAZYPAC_URL = "https://raw.githubusercontent.com/redwan-hossain/lazypac/main/lazypac.py"


def update_lazypac() -> None:
    if (os.path.exists(f"{BASE_DIR}/lazypac.py")):
        print(colored.cyan("\nDownloading lazypac from github repo...\n"))
        wget.download(LAZYPAC_URL, f"{BASE_DIR}/lazypac_updated.py")
        print("\n")

        with open(f"{BASE_DIR}/lazypac.py", "rb") as file:
            md5Hash_current = hashlib.md5(file.read())
            hash_of_current_lazypac: str = md5Hash_current.hexdigest()

        with open(f"{BASE_DIR}/lazypac_updated.py", "rb") as file:
            md5Hash_new = hashlib.md5(file.read())
            hash_of_updated_lazypac: str = md5Hash_new.hexdigest()

        if hash_of_current_lazypac != hash_of_updated_lazypac:
            os.remove(f"{BASE_DIR}/lazypac.py")
            os.rename(f"{BASE_DIR}/lazypac_updated.py", f"{BASE_DIR}/lazypac.py")
            print(colored.yellow("Lazypac has been updated."))
        else:
            os.system(f"rm {BASE_DIR}/lazypac.py")
            print(colored.yellow("Lazypac is up to date."))


def clear_console() -> None:
    os.system("clear")


def list_menu_input_handler() -> int:
    while True:
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print(colored.red("Invalid input. Try again"))
        else:
            return choice


def package_viewer_menu() -> int:
    print("\n")
    print(colored.cyan("1. All Packages"))
    print(colored.cyan("2. System Packages + Explicitly Installed"))
    print(colored.cyan("3. Explicitly Installed"))
    print(colored.cyan("4. Dependencies or Orphans"))
    print(colored.yellow("0. Back"))
    choice_input = list_menu_input_handler()
    return choice_input


def show_installed_packages() -> None:
    while True:
        choice_input = package_viewer_menu()
        match choice_input:
            case 0:
                break
            case 1:
                clear_console()
                os.system("pacman -Q")
            case 2:
                clear_console()
                os.system("pacman -Qe")
            case 3:
                clear_console()
                os.system("pacman -Qet")
            case 4:
                clear_console()
                os.system("pacman -Qdt")


def orphan_pkg_remove_choice_input_handler() -> bool:
    while True:
        input_choice = input(
            "Do you want to uninstall orphan packages? (y/n): "
        ).lower()
        if input_choice not in ("y", "n"):
            print(colored.red("Invalid input. Try again."))
        else:
            return True if input_choice == "y" else False


def pkg_installer() -> None:
    pkg_name = input("enter package name: ")
    os.system(f"sudo -S pacman -S --needed {pkg_name}")
    print(colored.blue("DONE..."))


def pkg_uninstaller() -> None:
    pkg_name = input("enter package name: ")
    os.system(f"sudo -S pacman -R {pkg_name}")
    orphan_pkg_manage()


def orphan_pkg_manage() -> None:
    result = os.popen("pacman -Qdt").read()
    if result == "":
        print(colored.blue("No orphan package found"))
        print(colored.blue("DONE..."))
    else:
        print(colored.blue("\nOrphan package list:"))
        print(result)

        uninstall_choice = orphan_pkg_remove_choice_input_handler()
        if uninstall_choice:
            os.system("sudo -S pacman -R --noconfirm $(pacman -Qdtq)")
            print(colored.blue("DONE..."))


def pacman_cache_remove() -> None:
    os.system("sudo paccache -r")
    os.system("sudo paccache -ruk0")
    print(colored.blue("DONE..."))


def pkg_search() -> None:
    pkg_keyword = input("enter search keyword: ")
    os.system(f"pacman -Ss {pkg_keyword}")


def full_system_upgrade() -> None:
    os.system("sudo -S pacman -Syu")
    print(colored.blue("DONE..."))


def list_menu() -> int:
    print("\n")
    print(colored.blue("Lazypac- Pacman Simplifier for Lazy Pacman Users"))
    print(colored.green("1. Package Installer"))
    print(colored.green("2. Package Un-installer"))
    print(colored.green("3. Package Search"))
    print(colored.green("4. Full System Upgrade"))
    print(colored.green("5. Manage Orphan packages"))
    print(colored.green("6. Remove Pacman cache"))
    print(colored.green("7. Installed Packages"))
    print(colored.red("0. Exit"))
    print(colored.yellow("99. Check for Lazypac Update"))
    choice = list_menu_input_handler()
    return choice


def navigation() -> None:
    try:
        while True:
            choice_input = list_menu()
            match choice_input:
                case 0:
                    print(colored.blue("\nBYE..."))
                    break
                case 1:
                    pkg_installer()
                case 2:
                    pkg_uninstaller()
                case 3:
                    pkg_search()
                case 4:
                    full_system_upgrade()
                case 5:
                    orphan_pkg_manage()
                case 6:
                    pacman_cache_remove()
                case 7:
                    show_installed_packages()
                case 99:
                    update_lazypac()

    except KeyboardInterrupt:
        print(colored.blue("\nBYE..."))


if __name__ == "__main__":
    navigation()

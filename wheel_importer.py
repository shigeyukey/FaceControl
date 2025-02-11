import os
import sys
import time
import platform
import zipfile
import requests

from aqt import mw
from aqt.utils import showInfo, askUser, tooltip
from aqt.operations import QueryOp
from anki.utils import pointVersion

is_download_wheel = False

first_run = True

def download_wheel():

    ### shape_predictor.dat ###
    # Download from Fork of face_landmarks.dat.
    face_landmarks_dat = "https://github.com/shigeyukey/facial-landmarks-recognition/raw/refs/heads/master/shape_predictor_68_face_landmarks.dat"


    ### numpy wheel ###
    # win
    numpy_windows = "https://files.pythonhosted.org/packages/a5/89/3dbb820397d01ad3e8eb4aee6b6df97ecef46701e72d01d33d69e11fffde/numpy-1.21.0-cp39-cp39-win_amd64.whl"

    # mac
    numpy_mac = "https://files.pythonhosted.org/packages/46/6e/241ab0c4b69c44ae7e466384cb4499b238b23492d7b47b8f35065525ef68/numpy-1.21.0-cp39-cp39-macosx_10_9_universal2.whl"

    # linux
    numpy_linux = "https://files.pythonhosted.org/packages/33/56/f21ff9325b9c5b42e007f58e46e2eb20ba9d02c92788460ac7e21602ff79/numpy-1.21.0-cp39-cp39-manylinux_2_12_x86_64.manylinux2010_x86_64.whl"


    # Download and use dlib wheel.
    # https://github.com/alesanfra/dlib-wheels/tree/build-version-19-24-2

    ### dlib wheel ###
    # win
    dlib_windows = "https://files.pythonhosted.org/packages/58/b2/2e01cee8e3f607f3ba525aabcbf60e46ede116013fbba255c15d4ea066b4/dlib_bin-19.24.6-cp39-cp39-win_amd64.whl"

    # mac
    dlib_mac_x86_64 = "https://files.pythonhosted.org/packages/2d/87/727f04198a9695a97ef743c9a3fd57de4108003023018ddb922f300c1962/dlib_bin-19.24.6-cp39-cp39-macosx_10_9_x86_64.whl"

    dlib_mac_arm64 = "https://files.pythonhosted.org/packages/4c/d0/0e1ec0915b0ba53d5b52aefb98e1436716af22669d65f34ceff6127499b1/dlib_bin-19.24.6-cp39-cp39-macosx_11_0_arm64.whl"

    # linux
    dlib_linux_aarch64 = "https://files.pythonhosted.org/packages/fc/7a/b68c80189e67c1731543dfdbabac3836c57993b2978f4d241cd900ee000e/dlib_bin-19.24.6-cp39-cp39-manylinux_2_17_aarch64.manylinux2014_aarch64.whl"
    dlib_linux_x86_64 = "https://files.pythonhosted.org/packages/ec/5d/507dcbf04ca59bcb9ba785cbbb61ffca9922a85d8dc119739f9ae1fbff38/dlib_bin-19.24.6-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl"

    ### opencv-python (cv2) ###
    # https://pypi.org/project/opencv-python/#files

    # win
    cv2_win_amd64 = "https://files.pythonhosted.org/packages/a4/7d/f1c30a92854540bf789e9cd5dde7ef49bbe63f855b85a2e6b3db8135c591/opencv_python-4.11.0.86-cp37-abi3-win_amd64.whl"

    # mac
    cv2_macosx_13_0_x86_64 = "https://files.pythonhosted.org/packages/3b/84/0a67490741867eacdfa37bc18df96e08a9d579583b419010d7f3da8ff503/opencv_python-4.11.0.86-cp37-abi3-macosx_13_0_x86_64.whl"

    cv2_macosx_13_0_arm64 = "https://files.pythonhosted.org/packages/05/4d/53b30a2a3ac1f75f65a59eb29cf2ee7207ce64867db47036ad61743d5a23/opencv_python-4.11.0.86-cp37-abi3-macosx_13_0_arm64.whl"

    # linux
    cv2_manylinux2014_x86_64 = "https://files.pythonhosted.org/packages/2c/8b/90eb44a40476fa0e71e05a0283947cfd74a5d36121a11d926ad6f3193cc4/opencv_python-4.11.0.86-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl"

    cv2_manylinux2014_aarch64 = "https://files.pythonhosted.org/packages/f3/bd/29c126788da65c1fb2b5fb621b7fed0ed5f9122aa22a0868c5e2c15c6d23/opencv_python-4.11.0.86-cp37-abi3-manylinux_2_17_aarch64.manylinux2014_aarch64.whl"


    # pyautogui
    # pip install pyautogui --target path
    # This module does not have a C extension so it is put in Add-on in advance.
    # https://github.com/asweigart/pyautogui

    # NOTE: Remove the "mouseinfo" module because it's incompatible with Anki's PyQt (requires Tkinter)
    #       Error occurs on Linux, Winodows is fine.


    ### Pillow ### (it's needed for pyautogui.)
    # win
    pillow_win_arm64 = "https://files.pythonhosted.org/packages/95/56/97750bd33e68648fa432dfadcb8ede7624bd905822d42262d34bcebdd9d7/pillow-11.1.0-cp39-cp39-win_arm64.whl"

    # mac
    mac_pillow_arm64 = "https://files.pythonhosted.org/packages/a6/62/c7b359e924dca274173b04922ac06aa63614f7e934d132f2fe1d852509aa/pillow-11.1.0-cp39-cp39-macosx_11_0_arm64.whl"

    mac_pillow_x86_64 = "https://files.pythonhosted.org/packages/9a/1f/9df5ac77491fddd2e36c352d16976dc11fbe6ab842f5df85fd7e31b847b9/pillow-11.1.0-cp39-cp39-macosx_10_10_x86_64.whl"

    # linux
    linux_pillow_arm64 =  "https://files.pythonhosted.org/packages/0c/55/f182db572b28bd833b8e806f933f782ceb2df64c40e4d8bd3d4226a46eca/pillow-11.1.0-cp39-cp39-manylinux_2_28_aarch64.whl"

    linux_pillow_x86_64 = "https://files.pythonhosted.org/packages/75/fb/e330fdbbcbc4744214b5f53b84d9d8a9f4ffbebc2e9c2ac10475386e3296/pillow-11.1.0-cp39-cp39-manylinux_2_28_x86_64.whl"

    ### Mac pyobjc ###  (it's needed for pyautogui with Mac.)
    # Mac pyobjc-core
    mac_pyobjc_core_wheel = "https://files.pythonhosted.org/packages/14/ba/1c459d0f1fc4c80314040ea6efea433c0641adffa6701679ec3a917b51a3/pyobjc_core-11.0-cp39-cp39-macosx_10_9_universal2.whl"

    # pyobjc
    # https://github.com/ronaldoussoren/pyobjc
    # mac_pyobjc_wheel = "https://files.pythonhosted.org/packages/18/55/d0971bccf8a5a347eaccf8caa4718766a68281baab83d2b5e211b2767504/pyobjc-11.0-py3-none-any.whl"

    # pip install --platform macosx_11_0_arm64 --python-version 3.9 --target "C:\Users\shigg\AppData\Roaming\Anki2\addons21\Face Control simple\user_files\macOS" --only-binary=:all: pyobjc
    # NOTE: Control by pyautogu on Mac devices requires permission.


    ### linux python3-xlib ### (it's needed for pyautogui with linux.)
    # pip install python3-xlib --target path
    # This module does not have a C extension so it is put in Add-on in advance.
    # https://pypi.org/project/python3-xlib/#files


    # Select the appropriate Numpy and Cv2 for the platform.
    os_type = platform.system()
    machine_type = platform.machine()

    numpy_wheel = ""
    dlib_wheel = ""
    cv2_wheel = ""
    pillow_wheel = ""

    if os_type == "Windows":
        numpy_wheel = numpy_windows
        dlib_wheel = dlib_windows
        cv2_wheel = cv2_win_amd64
        pillow_wheel = pillow_win_arm64

    elif os_type == "Linux":
        numpy_wheel = numpy_linux
        if machine_type == "x86_64":
            dlib_wheel = dlib_linux_x86_64
            cv2_wheel = cv2_manylinux2014_x86_64
            pillow_wheel = linux_pillow_x86_64

        elif machine_type == "aarch64":
            dlib_wheel = dlib_linux_aarch64
            cv2_wheel = cv2_manylinux2014_aarch64
            pillow_wheel = linux_pillow_arm64

    elif os_type == "Darwin":

        if machine_type == "x86_64":
            numpy_wheel = numpy_mac
            dlib_wheel = dlib_mac_x86_64
            cv2_wheel = cv2_macosx_13_0_x86_64
            pillow_wheel = mac_pillow_x86_64

        elif machine_type == "arm64":
            numpy_wheel = numpy_mac
            dlib_wheel = dlib_mac_arm64
            cv2_wheel = cv2_macosx_13_0_arm64
            pillow_wheel = mac_pillow_arm64

    # Save the wheels in user_files.
    addon_path = os.path.dirname(__file__)
    wheels_folder = os.path.join(addon_path, "user_files")
    resources_folder = os.path.join(addon_path,  "user_files", "resources")

    if not os.path.exists(wheels_folder):
        os.makedirs(wheels_folder)

    if not os.path.exists(resources_folder):
        os.makedirs(resources_folder)

    # Create paths (Numpy, Dlib, Cv2, Pollow)
    numpy_wheel_path = os.path.join(wheels_folder, f"numpy_{os_type}_{machine_type}.whl")
    dlib_wheel_path = os.path.join(wheels_folder, f"dlib_{os_type}_{machine_type}.whl")
    cv2_wheel_path = os.path.join(wheels_folder, f"cv2_{os_type}_{machine_type}.whl")
    pillow_wheel_path = os.path.join(wheels_folder, f"pillow_{os_type}_{machine_type}.whl")

    # Create paths (for Mac, pyobjc)
    mac_pyobjc_core_wheel_path = ""
    mac_pyobjc_wheel_path = ""
    if os_type == "Darwin":
        mac_pyobjc_core_wheel_path = os.path.join(wheels_folder, f"pyobjc_core_{os_type}_{machine_type}.whl")
        mac_pyobjc_wheel_path = os.path.join(wheels_folder, f"pyobjc_{os_type}_{machine_type}.whl")

    # Create paths (shape_predictor)
    face_landmarks_dat_path = os.path.join(resources_folder, f"shape_predictor.dat")

    # Download Wheels
    if numpy_wheel:
        with requests.get(numpy_wheel, stream=True) as r:
            with open(numpy_wheel_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    f.write(chunk)

    if dlib_wheel:
        with requests.get(dlib_wheel, stream=True) as r:
            with open(dlib_wheel_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    f.write(chunk)

    if cv2_wheel:
        with requests.get(cv2_wheel, stream=True) as r:
            with open(cv2_wheel_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    f.write(chunk)

    if pillow_wheel:
        with requests.get(pillow_wheel, stream=True) as r:
            with open(pillow_wheel_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    f.write(chunk)


    if os_type == "Darwin": # Mac
        if mac_pyobjc_core_wheel: # pyobjc-core
            with requests.get(mac_pyobjc_core_wheel, stream=True) as r:
                with open(mac_pyobjc_core_wheel_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024*1024):
                        f.write(chunk)
        # if mac_pyobjc_wheel: # pyobjc
        #     with requests.get(mac_pyobjc_wheel, stream=True) as r:
        #         with open(mac_pyobjc_wheel_path, 'wb') as f:
        #             for chunk in r.iter_content(chunk_size=1024*1024):
        #                 f.write(chunk)


    # shape_predictor.dat
    with requests.get(face_landmarks_dat, stream=True) as r:
        with open(face_landmarks_dat_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                f.write(chunk)

    return (numpy_wheel_path, dlib_wheel_path, cv2_wheel_path,
            pillow_wheel_path, mac_pyobjc_core_wheel_path )
            # pillow_wheel_path, mac_pyobjc_core_wheel_path, mac_pyobjc_wheel_path )

def add_lib_folder_to_sys():
    # Add the lib folder to sys.path
    addon_path = os.path.dirname(__file__)
    lib_folder = os.path.join(addon_path, "user_files" , "lib") # downloaded modules
    pyautogui_lib_folder = os.path.join(addon_path, "lib", "pyautogui_lib") # pyautogui

    python3_xlib_folder = os.path.join(addon_path, "lib", "python3_xlib_lib") # python3_xlib (linux)
    mac_lib_folder =  os.path.join(addon_path, "lib", "mac_lib") # pyobjc (Mac)

    if lib_folder not in sys.path:
        # First, import the downloaded modules.
        sys.path.insert(0, lib_folder)

    if platform.system() == "Linux":
        # python3_xlib is only needed on Linux.
        if python3_xlib_folder not in sys.path:
            sys.path.insert(0, python3_xlib_folder)

    if platform.system() == "Darwin":
        if mac_lib_folder not in sys.path:
            sys.path.insert(0, mac_lib_folder)

    if pyautogui_lib_folder not in sys.path:
        # Next, import the pyautogui included in the add-on.
        sys.path.insert(0, pyautogui_lib_folder)


def unzipped_module():
    # Save the unzipped module in user_files.
    addon_path = os.path.dirname(__file__)
    lib_folder = os.path.join(addon_path, "user_files" , "lib")

    if not os.path.exists(lib_folder):
        (numpy_wheel_path, dlib_wheel_path, cv2_wheel_path,
        pillow_wheel_path, mac_pyobjc_core_wheel_path) = download_wheel()
        # pillow_wheel_path, mac_pyobjc_wheel_path, mac_pyobjc_core_wheel_path) = download_wheel()

        def extract_wheel(wheel_path, extract_to):
            with zipfile.ZipFile(wheel_path, "r") as zip_ref:
                zip_ref.extractall(extract_to)

        if os.path.exists(numpy_wheel_path) and os.path.exists(dlib_wheel_path):
            os.makedirs(lib_folder)

            # Unzip wheels
            extract_wheel(numpy_wheel_path, lib_folder)
            extract_wheel(dlib_wheel_path, lib_folder)
            extract_wheel(cv2_wheel_path, lib_folder)
            extract_wheel(pillow_wheel_path, lib_folder)

            if platform.system() == "Darwin":
                extract_wheel(mac_pyobjc_core_wheel_path, lib_folder)
                # extract_wheel(mac_pyobjc_wheel_path, lib_folder)

            # After unzipping wheels, delete wheels.
            os.remove(numpy_wheel_path)
            os.remove(dlib_wheel_path)
            os.remove(cv2_wheel_path)
            os.remove(pillow_wheel_path)

            if platform.system() == "Darwin":
                os.remove(mac_pyobjc_core_wheel_path)
                # os.remove(mac_pyobjc_wheel_path)

            # Wait a bit until extract is complete.
            time.sleep(1)

    add_lib_folder_to_sys()


def check_imports():
    # Checks if the modules import is successful.
    try:
        import numpy
        import dlib # type: ignore
        import cv2 # type: ignore
        import PIL
        addon_path = os.path.dirname(__file__)
        resources_folder = os.path.join(addon_path, "user_files", "resources", "shape_predictor.dat")
        if not os.path.exists(resources_folder):
            return False
        return True
    except ImportError as e:
        print("ImportError", e)
        return False

def get_is_download_wheel():
    return is_download_wheel

def on_success(result):
    # Show a message box if the download is successful.
    global is_download_wheel
    is_download_wheel = False
    if check_imports():
        showInfo(text="Download Complete!", parent=mw, title="Face Control")
    else:
        showInfo(text="Error: Download failed.", parent=mw, title="Face Control", type="warning")

def import_module():
    addon_path = os.path.dirname(__file__)
    lib_folder = os.path.join(addon_path, "user_files" , "lib")

    yes = True
    # If the module folder is not yet available, download them.
    if not os.path.exists(lib_folder):
        yes = askUser(text="Module not found.\n Do you want to start downloading?", parent=mw, title="Face Control")
        if yes:
            global is_download_wheel
            is_download_wheel = True

            # Download modules in the background using Anki's QueryOp
            op = QueryOp(
                parent=mw,
                op=lambda col: unzipped_module(),
                success=on_success,
            )

            if pointVersion() >= 231000:
                # Using "without_collection" may speed up the process a bit.
                op.without_collection()
            op.run_in_background()
    else:
        # Already downloaded, add the lib folder to sys.path
        add_lib_folder_to_sys()

    return yes


def run_wheel_importer():
    global first_run
    if first_run:
        # Download will start only the first time.
        yes = import_module()
        if yes:
            first_run = False

    if get_is_download_wheel():
        # Download is not finished yet.
        tooltip("Now loading, please wait...")
        return False

    if not check_imports():
        # If import fails.
        tooltip("Error: Module import failed.")
        return False

    # If import is successful.
    return True
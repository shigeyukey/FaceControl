import os
import sys
import time
import platform
import zipfile
import requests

from aqt import mw
from aqt.utils import showInfo, askUser
from aqt.operations import QueryOp
from anki.utils import pointVersion

is_download_wheel = False

def download_wheel():

    # Download from Fork of face_landmarks.dat.
    face_landmarks_dat = "https://github.com/shigeyukey/facial-landmarks-recognition/raw/refs/heads/master/shape_predictor_68_face_landmarks.dat"

    # numpy wheel
    numpy_windows = "https://files.pythonhosted.org/packages/a5/89/3dbb820397d01ad3e8eb4aee6b6df97ecef46701e72d01d33d69e11fffde/numpy-1.21.0-cp39-cp39-win_amd64.whl"
    numpy_mac = "https://files.pythonhosted.org/packages/46/6e/241ab0c4b69c44ae7e466384cb4499b238b23492d7b47b8f35065525ef68/numpy-1.21.0-cp39-cp39-macosx_10_9_universal2.whl"
    numpy_linux = "https://files.pythonhosted.org/packages/33/56/f21ff9325b9c5b42e007f58e46e2eb20ba9d02c92788460ac7e21602ff79/numpy-1.21.0-cp39-cp39-manylinux_2_12_x86_64.manylinux2010_x86_64.whl"


    # Download and use dlib wheel.
    # https://github.com/alesanfra/dlib-wheels/tree/build-version-19-24-2

    # dlib wheel
    dlib_windows = "https://files.pythonhosted.org/packages/58/b2/2e01cee8e3f607f3ba525aabcbf60e46ede116013fbba255c15d4ea066b4/dlib_bin-19.24.6-cp39-cp39-win_amd64.whl"

    dlib_mac_x86_64 = "https://files.pythonhosted.org/packages/2d/87/727f04198a9695a97ef743c9a3fd57de4108003023018ddb922f300c1962/dlib_bin-19.24.6-cp39-cp39-macosx_10_9_x86_64.whl"
    dlib_mac_arm64 = "https://files.pythonhosted.org/packages/4c/d0/0e1ec0915b0ba53d5b52aefb98e1436716af22669d65f34ceff6127499b1/dlib_bin-19.24.6-cp39-cp39-macosx_11_0_arm64.whl"

    dlib_linux_aarch64 = "https://files.pythonhosted.org/packages/fc/7a/b68c80189e67c1731543dfdbabac3836c57993b2978f4d241cd900ee000e/dlib_bin-19.24.6-cp39-cp39-manylinux_2_17_aarch64.manylinux2014_aarch64.whl"
    dlib_linux_x86_64 = "https://files.pythonhosted.org/packages/ec/5d/507dcbf04ca59bcb9ba785cbbb61ffca9922a85d8dc119739f9ae1fbff38/dlib_bin-19.24.6-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl"

    os_type = platform.system()
    machine_type = platform.machine()

    if os_type == "Windows":
        numpy_wheel = numpy_windows
        dlib_wheel = dlib_windows
    elif os_type == "Linux":
        numpy_wheel = numpy_linux
        if machine_type == "x86_64":
            dlib_wheel = dlib_linux_x86_64
        elif machine_type == "aarch64":
            dlib_wheel = dlib_linux_aarch64
        else:
            dlib_wheel = ""
    elif os_type == "Darwin":
        if machine_type == "x86_64":
            numpy_wheel = numpy_mac
            dlib_wheel = dlib_mac_x86_64
        elif machine_type == "arm64":
            numpy_wheel = numpy_mac
            dlib_wheel = dlib_mac_arm64
        else:
            dlib_wheel = ""

    addon_path = os.path.dirname(__file__)
    wheels_folder = os.path.join(addon_path, "user_files")
    resources_folder = os.path.join(addon_path,  "user_files", "resources")

    if not os.path.exists(wheels_folder):
        os.makedirs(wheels_folder)

    if not os.path.exists(resources_folder):
        os.makedirs(resources_folder)

    numpy_wheel_path = os.path.join(wheels_folder, f"numpy_{os_type}_{machine_type}.whl")
    dlib_wheel_path = os.path.join(wheels_folder, f"dlib_{os_type}_{machine_type}.whl")

    face_landmarks_dat_path = os.path.join(resources_folder, f"shape_predictor.dat")

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

    with requests.get(face_landmarks_dat, stream=True) as r:
        with open(face_landmarks_dat_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                f.write(chunk)

    return numpy_wheel_path, dlib_wheel_path

def unzipped_module():
    # Save the unzipped module in user_files
    addon_path = os.path.dirname(__file__)
    lib_folder = os.path.join(addon_path, "user_files" , "lib")

    if not os.path.exists(lib_folder):
        numpy_wheel_path, dlib_wheel_path = download_wheel()

        def extract_wheel(wheel_path, extract_to):
            with zipfile.ZipFile(wheel_path, "r") as zip_ref:
                zip_ref.extractall(extract_to)

        if os.path.exists(numpy_wheel_path) and os.path.exists(dlib_wheel_path):
            os.makedirs(lib_folder)
            extract_wheel(numpy_wheel_path, lib_folder)
            extract_wheel(dlib_wheel_path, lib_folder)

            os.remove(numpy_wheel_path)
            os.remove(dlib_wheel_path)

            # Wait a bit until extract is complete.
            time.sleep(1)

    # Add the lib folder to sys.path
    if lib_folder not in sys.path:
        sys.path.insert(0, lib_folder)

def check_imports():
    try:
        import numpy
        import dlib
        addon_path = os.path.dirname(__file__)
        resources_folder = os.path.join(addon_path,  "user_files", "resources", "shape_predictor.dat")
        if not os.path.exists(resources_folder):
            return False
        return True
    except ImportError:
        return False

def get_is_download_wheel():
    return is_download_wheel

def on_success(result):
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
    if not os.path.exists(lib_folder):
        yes = askUser(text="Module not found.\n Do you want to start downloading?", parent=mw, title="Face Control")
        if yes:
            global is_download_wheel
            is_download_wheel = True
            op = QueryOp(
                parent=mw,
                op=lambda col: unzipped_module(),
                success=on_success,
            )

            if pointVersion() >= 231000:
                op.without_collection()
            op.run_in_background()

    else:
        if lib_folder not in sys.path:
            sys.path.insert(0, lib_folder)

    return yes
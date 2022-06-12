import time
import sys

import psutil
import win32gui
import win32process
from pycaw.pycaw import AudioUtilities


def get_config():
    process_name_list = ["YuanShen.exe", "GenshinImpact.exe"]
    file_name = "BackgroundMuter.txt"
    encoding = "utf-8"
    try:
        process_name_list = open(file_name, "r", encoding=encoding).read().strip().split("\n")
    except:
        open(file_name, "w", encoding=encoding).write("\n".join(process_name_list))
    return process_name_list


background_mute_process = get_config()

def unset_mute():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        pname = session.Process.name() if session.Process else None
        if not pname:  # @%SystemRoot%\\System32\\AudioSrv.Dll,-202
            continue

        volume = session.SimpleAudioVolume
        if pname in background_mute_process:
            volume.SetMute(False, None)
            print(f"{pname} SetMute False")
            return True
    return False

def main():
    print("Background mute process:", background_mute_process)
    while True:
        pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())  # type: ignore
        if pid[0] == 0:
            print("No foreground window")
            time.sleep(0.5)
            continue
        foreground_name = psutil.Process(pid[-1]).name()
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            pname = session.Process.name() if session.Process else None
            if not pname:  # @%SystemRoot%\\System32\\AudioSrv.Dll,-202
                continue

            volume = session.SimpleAudioVolume
            mute = foreground_name != pname
            is_mute = volume.GetMute()
            is_changed = is_mute != mute

            if pname in background_mute_process:
                if is_changed:
                    volume.SetMute(mute, None)
                    print(f"{pname} SetMute {mute}")
                time.sleep(0.5)


if __name__ == "__main__":
    try:
        if len(sys.argv)>1:
            unset_mute()
        else:
            main()
    except KeyboardInterrupt:
        print("Bye")

import win32gui
import time
import psutil
from pycaw.pycaw import AudioUtilities
import win32process

def get_config():
    process_name_list = ['YuanShen.exe']
    file_name = 'BackgroundMuter.txt'
    encoding = 'utf-8'
    try:
        process_name_list = open(file_name, "r", encoding=encoding).read().strip().split("\n")
    except:
        open(file_name, "w", encoding=encoding).write("\n".join(process_name_list))
    return process_name_list

def get_pid():
    pass

background_mute_process = get_config()
print("Background mute process:", background_mute_process)
while 1:
    pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    if pid[0] == 0:
        print("No foreground window")
        time.sleep(0.5)
        continue
    foreground_name = psutil.Process(pid[-1]).name()
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        pname = session.Process.name() if session.Process else None
        if not pname: # @%SystemRoot%\\System32\\AudioSrv.Dll,-202
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

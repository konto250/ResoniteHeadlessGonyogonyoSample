import subprocess
import time
import threading

def monitor_process(proc):
    # 標準出力を行ごとに読み取る
    for line in iter(proc.stdout.readline, ''):
        line = line.decode('utf-8', errors='ignore').strip()
        #line = line.decode('utf-8').strip()
        print(f"Output: {line}")
        if 'World running...' in line:
            print("Sending 'world' to process input...")
            proc.stdin.write(b'worlds\n')
            proc.stdin.flush()

def send_shutdown(proc):
    # 10分待つ
    time.sleep(10*60)
    print("10 minutes passed. Sending 'shutdown' to process input...")
    proc.stdin.write(b'shutdown\n')
    proc.stdin.flush()

if __name__ == "__main__":
    PROGRAM_PATH = 'C:/Program Files (x86)/Steam/steamapps/common/Resonite/Headless/Resonite.exe'
    OPTIONS = ['headlessconfig', 'Config/Config01.json', '-LoadAssembly', '../Libraries/ResoniteModLoader.dll']
    CWD_PATH = 'C:/Program Files (x86)/Steam/steamapps/common/Resonite/Headless/'

    # プログラムを起動
    command = [PROGRAM_PATH] + OPTIONS
    proc = subprocess.Popen(command, 
                            stdin=subprocess.PIPE, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE, 
                            cwd=CWD_PATH, 
                            text=False, 
                            # bufsize=1,
                            universal_newlines=False)

    # 標準出力の監視スレッドを開始
    thread1 = threading.Thread(target=monitor_process, args=(proc,))
    thread1.start()

    # 10分後の処理のためのスレッドを開始
    thread2 = threading.Thread(target=send_shutdown, args=(proc,))
    thread2.start()

    # スレッドが終了するまで待つ
    thread1.join()
    thread2.join()

    # プログラムが終了するのを待つ
    proc.communicate()

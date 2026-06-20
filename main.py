import subprocess
import sys
from pathlib import Path


def main():
    root = Path(__file__).parent

    fun_proc = subprocess.Popen([sys.executable, 'main.py'], cwd=root / 'fun_bot')
    lol_proc = subprocess.Popen([sys.executable, 'main.py'], cwd=root / 'lol_bot')

    try:
        fun_proc.wait()
        lol_proc.wait()
    except KeyboardInterrupt:
        fun_proc.terminate()
        lol_proc.terminate()
        fun_proc.wait()
        lol_proc.wait()


if __name__ == '__main__':
    main()

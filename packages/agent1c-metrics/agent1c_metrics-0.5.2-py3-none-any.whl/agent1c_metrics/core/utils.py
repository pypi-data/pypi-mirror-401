import subprocess
import sys
import os

def upgrade_and_restart():
    # 1. Обновляем модуль
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "agent1c_metrics"])
        print("Обновление завершено успешно")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при обновлении: {e}")
        return
    
    # Даем небольшую паузу, чтобы файловая система "остыла"
    import time
    time.sleep(2)

    # 2. Перезапуск
    restart_process()

def restart_process():
    # Если вы знаете имя службы в Windows:
    # subprocess.Popen(["net", "stop", "agent1c_metrics", "&&", "net", "start", "agent1c_metrics"], shell=True)
    
    # Или просто жестко завершаем процесс, WinSW сам его поднимет (если настроен рестарт)
    print("Forcing immediate exit for WinSW...")
    # Очищаем буферы вывода, чтобы принт успел записаться в файл
    sys.stdout.flush()
    # Жесткое завершение всего процесса
    os._exit(1)
import serial
import spidev
from time import sleep
import RPi.GPIO as GPIO
import os
import subprocess

#------------------
#このコードは動作確認用のテストコードです。後々作成します。
#TODO ボタンを押したら物理ボタン(つまみ)でのエフェクトの値変更を可能にする。
#------------------
# GPIOピンの設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # ボタン1
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # ボタン2
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # ボタン3

# 初期設定
preset = 0
preset_old = 0

# ファイル読み取りとエラーハンドリング
try:
    with open("/ben/Desktop/rpieffectbox/names.txt") as name_file:
        names = name_file.read().splitlines()
except FileNotFoundError:
    print("Error: names.txt not found.")
    names = []

try:
    with open("/ben/Desktop/rpieffectbox/functions.txt") as function_file:
        functions = function_file.read().splitlines()
except FileNotFoundError:
    print("Error: functions.txt not found.")
    functions = []

# SPIの初期化
try:
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 1350000
except Exception as e:
    print(f"Error initializing SPI: {e}")

# シリアル通信の初期化
try:
    ser = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=1)
except serial.SerialException as e:
    print(f"Error initializing serial: {e}")

def readadc(adcnum):
    """SPIを使ってMCP3008の指定チャネルから値を読み取る"""
    if 0 <= adcnum <= 7:
        r = spi.xfer2([1, (8 + adcnum) << 4, 0])
        adcout = ((r[1] & 3) << 8) + r[2]
        return adcout
    else:
        return -1

def start_pd():
    """Pure Dataプロセスの起動（重複を防止）"""
    if not is_pd_running():
        subprocess.Popen(["pd", "-nogui", "server.pd"])
        sleep(2)  # 起動待機

def is_pd_running():
    """Pure Dataプロセスが既に実行中か確認"""
    result = subprocess.run(["pgrep", "-f", "pd -nogui"], stdout=subprocess.PIPE)
    return result.returncode == 0

def send_to_pd(channel, value):
    """Pure Dataに値を送信"""
    subprocess.run(["pdsend", "5001", "localhost", "udp"], input=f"{channel} {value};", text=True)

def update_display():
    """シリアルディスプレイの更新"""
    try:
        ser.write(f"?f{names[preset]}?n{functions[preset]}\n".encode('utf-8'))
    except IndexError:
        print("Error: Invalid preset index.")

# 初期メッセージの送信
try:
    ser.write("?fRaspberry Pi?nEffects Module\n".encode('utf-8'))
    sleep(1)
    ser.write("?fBuilt By ?nBen Jacobs\n".encode('utf-8'))
    sleep(2)
    ser.write("?fOpening PD...\n".encode('utf-8'))
    sleep(2)
    start_pd()
    update_display()
except Exception as e:
    print(f"Error during initialization: {e}")

# メインループ
while True:
    sleep(0.01)  # CPU負荷を軽減

    # プリセット切り替え（ボタン17と18）
    if GPIO.input(17) and preset > 0:
        preset_old = preset
        preset -= 1
        send_to_pd(1, preset_old)
        send_to_pd(0, preset)
        update_display()

    elif GPIO.input(18) and preset < len(names) - 1:
        preset_old = preset
        preset += 1
        send_to_pd(1, preset_old)
        send_to_pd(0, preset)
        update_display()

    # エフェクト値の調整モード（ボタン4）
    elif GPIO.input(4):
        ser.write("?f\n".encode('utf-8'))
        sleep(0.2)
        while True:
            value0 = readadc(0)
            value1 = readadc(1)
            value2 = readadc(2)
            value3 = readadc(3)

            send_to_pd(3, value0)
            send_to_pd(0, value1)
            send_to_pd(1, value2)
            send_to_pd(2, value3)

            ser.write(f"?fE1:{value3} E2:{value2}?nE3:{value1} E4:{value0}\n".encode('utf-8'))
            
            if GPIO.input(4):  # ボタン4でモード終了
                sleep(0.2)
                update_display()
                break

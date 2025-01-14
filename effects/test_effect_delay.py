class delay():
 def __init__(self):
   pass
 def set_delay_time(self,address, *args):
    global delay_time  # 範囲: 0.1〜2.0
    delay_time=((args[0] + 1) / 10)
    print(f"Delay time set to: {delay_time}")
    return delay_time
 def set_delay_feedback(self,address, *args):
    global delay_feedback
    delay_feedback = ((args[0]) / 10) # 範囲: 0.0〜0.9
    print(f"Delay Feedback set to: {delay_feedback}")
    return delay_feedback
#returnを使用して動作不良が起きたらコメントアウト
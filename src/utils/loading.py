import threading, sys, time

def start():
    spin_thread = threading.Thread(target=spinner)
    spin_thread.do_run = True
    spin_thread.daemon = True  # Ensures spinner stops if main thread exits
    spin_thread.start()
    return spin_thread

def stop(spin_thread):
    spin_thread.do_run = False
    sys.stdout.write("\r")  # Clear the spinner
    sys.stdout.flush()

def spinner():
    ''' Spinner on terminal during analysis'''
    rotation = ["|", "/", "-", "\\"]
    for _ in range(100):  # Arbitrary high number to keep it running
        for frame in rotation:
            sys.stdout.write(f"\r{frame}")  # Overwrite the line with the current frame
            sys.stdout.flush()
            time.sleep(0.1)  # Pause to make the rotation visible

def loading_bar(current, total):
    percent = (current / total) * 100
    bar_length = 40  # Length of the loading bar
    filled_length = int(bar_length * current // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\r\n{current} of {total} |{bar}| {percent:.2f}%')
    sys.stdout.flush()
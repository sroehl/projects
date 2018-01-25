import librtmp
import urllib.request
import json
import ssl
import cv2
import sys
import threading
import subprocess
import time
import os
from image_cv import compare_images

def get_url():
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE
	resp = urllib.request.urlopen("https://1z3-devmng2.myzmodo.com/device/rtmp?callback=jQuery21400985808377710613_1513709495924&tokenid=3tg1mbem0vj8ca8brha2n0i687&physical_id=ZMD13I5DA260228&media_type=0&channel_num=0&record_cloud=1&_=1513709495925", context=ctx)
	data = resp.read()
	encoding = resp.info().get_content_charset('utf-8')
	decoded = data.decode(encoding)
	jsonData = json.loads(decoded[decoded.index('{'):-1])
	if 'ip' in jsonData:
		return 'rtmp://{}:{}/live/{}?code={}'.format(jsonData['ip'], jsonData['port'], jsonData['stream_id'], jsonData['code'])
	return None

def run_ffmpeg():
    global running
    folder = 'cam_images' + os.sep
    image_name = folder + '%03d.jpg'
    try:
        os.mkdir(folder)
    except FileExistsError:
        pass
    FNULL = open(os.devnull, 'w')
    process = None
    while running:
        if process is None:
            process =  subprocess.Popen(['ffmpeg', '-i',url, '-r', '2', image_name], stdout=FNULL, stderr=subprocess.STDOUT)
        running = False
        time.sleep(60)
    process.kill()

def get_last_two_names():
    highest = 0
    for f in os.listdir('cam_images'):
        if os.path.isfile(os.path.join('cam_images',f)):
            num = f.split('.')[0]
            num = int(num)
            if num > highest:
                highest = num
    return ("{:03d}.jpg".format(highest-1), "{:03d}.jpg".format(highest))


url = get_url()
print(url)
running = True
ffmpeg_thread = threading.Thread(target=run_ffmpeg)
ffmpeg_thread.start()
try:
    for i in range(0,60):
        started = time.time()
        last_name, one_from_last_name = get_last_two_names()
        last_path = os.path.join('cam_images', last_name)
        last = cv2.imread(last_path, 0)
        one_from_last_path = os.path.join('cam_images', one_from_last_name)
        one_from_last = cv2.imread(one_from_last_path, 0)
        if last is not None and one_from_last is not None:
            compare_images(last, one_from_last)
        else:
            print("Problem opening images")
        end = time.time()
        print("took: {}".format(end-started))
        time.sleep(1)
finally:
    running = False
    time.sleep(1)
    print("Done")



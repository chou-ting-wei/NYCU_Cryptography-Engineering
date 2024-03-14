import hashlib
import time
import requests

def download_file(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        return response.content
    else:
        return None

def calculate_hash(hash_function, data):
    start_time = time.time()
    hash_obj = hashlib.new(hash_function)
    hash_obj.update(data)
    end_time = time.time()
    return end_time - start_time

url = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
video_data = download_file(url)

if video_data:
    hash_functions = ["md5", "sha1", "sha224", "sha256", "sha512", "sha3_224", "sha3_256", "sha3_512"]
    times = {}

    for func in hash_functions:
        times[func] = calculate_hash(func, video_data)

    sorted_times = sorted(times.items(), key=lambda x: x[1])

    for func, time_taken in sorted_times:
        print(f"{func}: {time_taken:.5f} seconds")
else:
    print("Failed to download the video file.")
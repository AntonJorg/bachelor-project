import os
import requests
import subprocess

dir_path = os.path.join("data", "original")
file_name = "positions.data"

URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/connect-4/connect-4.data.Z"

print(f"Downloading position database into {dir_path} from:\n{URL}\n")
print("If something goes wrong, data and more info can be found at https://archive.ics.uci.edu/ml/machine-learning-databases/connect-4/\n")

if file_name in os.listdir(dir_path):
    print(f"File {file_name} already in {dir_path}, skipping download.")
else:
    path = os.path.join(dir_path, file_name + ".Z")

    response = requests.get(URL)

    with open(path, "wb") as f:
        f.write(response.content)

    print("Position database Z archive successfully downloaded, unpacking...")

    subprocess.run(["uncompress", path])

    print("Position database successfully unpacked!")

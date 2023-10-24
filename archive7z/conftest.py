import pytest
import yaml
import random
import string
from datetime import datetime
from sshcheckers import ssh_checkout, ssh_getout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return ssh_checkout(data["ip"], data["user"], data["passwd"],
                        "mkdir {} {} {} {}".format(data["folder_in"], data["folder_out"], data["folder_ext"],
                                                   data["folder_ext2"]), "")


@pytest.fixture()
def clear_folders():
    return ssh_checkout(data["ip"], data["user"], data["passwd"],
                        "rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_out"],
                                                            data["folder_ext"], data["folder_ext2"]), "")


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout(data["ip"], data["user"], data["passwd"],
                        "cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"],
                                                                                               filename, data["bs"]),
                        ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout(data["ip"], data["user"], data["passwd"],
                        "cd {}; mkdir {}".format(data["folder_in"], subfoldername), ""):
        return None, None
    if not ssh_checkout(data["ip"], data["user"], data["passwd"],
                        "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_in"],
                                                                                                  subfoldername,
                                                                                                  testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture(autouse=True)
def print_time():
    yield print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    print("Finish: {}".format(datetime.now().strftime("%H:%M:%S.%f")))


@pytest.fixture(autouse=True)
def stat():
    yield
    stat = ssh_getout(data["ip"], data["user"], data["passwd"], "cat /proc/loadavg")
    ssh_checkout(data["ip"], data["user"], data["passwd"],
                 "echo 'time: {} count:{} size: {} load: {}'>> stat.txt".format(
                     datetime.now().strftime("%H:%M:%S.%f"), data["count"], data["bs"], stat), "")

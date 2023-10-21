from sshcheckers import ssh_checkout, ssh_getout
import yaml

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:
    def test_step1(self, make_folders, clear_folders, make_files):
        # test1
        res = []
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                f"cd {data['folder_in']}; 7z a {data['folder_out']}/arch1 -t{data['type']}",
                                "Everything is Ok"))
        res.append(
            ssh_checkout(data["ip"], data["user"], data["passwd"], f"ls {data['folder_out']}", f"arch1.{data['type']}"))
        assert all(res), "test1 FAIL"

    def test_step2(self, clear_folders, make_files):
        # test2
        res = []
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                f"cd {data['folder_in']}; 7z a {data['folder_out']}/arch1 -t{data['type']}",
                                "Everything is Ok"))
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                f"cd {data['folder_out']}; 7z e arch1.{data['type']} -o{data['folder_ext']} -y",
                                "Everything is Ok"))

        for item in make_files:
            res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], f"ls {data['folder_ext']}", item))
        assert all(res), "test2 FAIL"

    def test_step3(self):
        # test3
        assert ssh_checkout(data["ip"], data["user"], data["passwd"],
                            f"cd {data['folder_out']}; 7z t arch1.{data['type']}",
                            "Everything is Ok"), "test3 FAIL"

    def test_step4(self):
        # test4
        assert ssh_checkout(data["ip"], data["user"], data["passwd"],
                            f"cd {data['folder_out']}; 7z u arch1.{data['type']}",
                            "Everything is Ok"), "test4 FAIL"

    def test_step5(self, clear_folders, make_files):
        # test5
        res = []
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                f"cd {data['folder_in']}; 7z a {data['folder_out']}/arch1 -t{data['type']}",
                                "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                    f"cd {data['folder_out']}; 7z l arch1.{data['type']}", item))
        assert all(res), "test5 FAIL"

    def test_step6(self, clear_folders, make_files, make_subfolder):
        res = []
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                f"cd {data['folder_in']}; 7z a {data['folder_out']}/arch1 -t{data['type']}",
                                "Everything is Ok"))
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                f"cd {data['folder_out']}; 7z x arch1.{data['type']} -o{data['folder_ext2']} -y",
                                "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], f"ls {data['folder_ext2']}", item))
        res.append(
            ssh_checkout(data["ip"], data["user"], data["passwd"], f"ls {data['folder_ext2']}", make_subfolder[0]))
        res.append(
            ssh_checkout(data["ip"], data["user"], data["passwd"], f"ls {data['folder_ext2']}/{make_subfolder[0]}",
                         make_subfolder[1]))
        assert all(res), "test6 FAIL"

    def test_step7(self):
        # test7
        assert ssh_checkout(data["ip"], data["user"], data["passwd"],
                            f"cd {data['folder_out']}; 7z d arch1.{data['type']}",
                            "Everything is Ok"), "test7 FAIL"

    def test_step8(self, clear_folders, make_files):
        # test8
        res = []
        for item in make_files:
            res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], f"cd {data['folder_in']}; 7z h {item}",
                                    "Everything is Ok"))
            hash = ssh_getout(data["ip"], data["user"], data["passwd"], f"cd {data['folder_in']}; crc32 {item}").upper()
            res.append(
                ssh_checkout(data["ip"], data["user"], data["passwd"], f"cd {data['folder_in']}; 7z h {item}", hash))
        assert all(res), "test8 FAIL"

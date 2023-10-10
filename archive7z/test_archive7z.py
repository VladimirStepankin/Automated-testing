from checkers import checkout, getout

folder_in = "/home/artanetz/tst"
folder_out = "/home/artanetz/folder_out"
folder_ext = "/home/artanetz/folder1"


def test_step1():
    # test1
    assert checkout(f"cd {folder_in}; 7z a {folder_out}/arch1", "Everything is Ok"), "test1 FAIL"


def test_step2():
    # test2
    assert checkout(f"cd {folder_out}; 7z d ./arch1.7z file1.txt", "Everything is Ok"), "test2 FAIL"


def test_step3():
    # test3
    assert checkout(f"cd {folder_out}; 7z l arch1.7z", "file2.txt"), "test3 FAIL"


def test_step4():
    # test4
    assert checkout(f"cd {folder_out}; 7z x arch1.7z -o{folder_ext} -y", "Everything is Ok"), "test4 FAIL"
    assert checkout(f"ls {folder_ext}", "file2.txt"), "test4 FAIL"


def test_step5():
    # test5
    res1 = checkout(f"cd {folder_in}; 7z h file1.txt", "")
    crc32_hash = getout(f"cd {folder_in}; crc32 test1.txt").upper()
    res2 = checkout(f"cd {folder_in}; 7z h file1.txt", crc32_hash)
    assert res1 and res2, "test5 FAIL"

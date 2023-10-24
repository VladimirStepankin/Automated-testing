from sshcheckers import ssh_checkout, upload_files
import yaml

with open("config.yaml", encoding='utf-8') as f:
    data = yaml.safe_load(f)


def deploy():
    res = []
    upload_files(data.get("ip"), data.get("user"), data.get("passwd"), "tests/p7zip-full.deb",
                 "/home/user2/p7zip-full.deb")
    res.append(ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"),
                            f'echo {data.get("passwd")} | sudo -S dpkg -i /home/user2/p7zip-full.deb',
                            "Настраивается пакет"))
    res.append(ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"),
                            f'echo {data.get("passwd")} | sudo -S dpkg -s {data.get("pkgname")}',
                            "Status: install ok installed"))
    return all(res)


if deploy():
    print("Деплой успешен")
else:
    print("Ошибка деплоя")
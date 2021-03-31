import subprocess

pid = subprocess.check_output('netstat.exe -aon | find "TCP"',
                              shell=True).split(bytes('\n', "cp1251"))
print("Введите диапазон из двух чисел через пробел:")
startDip, endDip = input().split()
list_ports = list()

for info in pid:
    try:
        parsed_ip = info.split()[1].split(bytes(':', "cp1251"))
        parsed_ip.reverse()
        port = parsed_ip[0]
    except:
        continue
    list_ports.append(port)

all_ports = list(set(list_ports))
filtered_ports = list()

for port in all_ports:
    if int(startDip) <= int(port) <= int(endDip):
        filtered_ports.append(port.decode("cp1251"))

filtered_ports.sort()
print("Открытые порты: " + str.join(", ", filtered_ports))
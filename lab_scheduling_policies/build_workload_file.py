from random import randint

def build_process_file():
    f = open('workload_file.ffd', 'w')
    proc_list = []
    timestamp_c = 1
    pid_c = 1

    for i in xrange(30):
        priority = randint(0, 127)
        service_time = randint(40, 400)
        proc_list.append(
            str(timestamp_c) + ' ' +
            str(pid_c) + ' ' +
            str(priority) + ' ' +
            str(service_time) + '\n'
        )
        timestamp_c += randint(1, 50)
        pid_c += 1

    f.writelines(proc_list)
    f.close()

if __name__ == '__main__':
    build_process_file()

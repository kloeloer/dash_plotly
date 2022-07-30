from flask import Flask
import psutil as ps
import datetime
import json
import socket

# get IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_addr = s.getsockname()[0]


app = Flask(__name__)


@app.route('/<get_info>')
def hello(get_info):
    if get_info == 'cpu_percent':
        data = ps.cpu_percent()
        hostname=socket.gethostname()
        my_ip = ps.net_if_addrs()['Wi-Fi'][1][1]
        tot_mem = ps.virtual_memory()[0]
        used_mem = ps.virtual_memory()[3]
        perc_mem = ps.virtual_memory()[2]
        cpu_frequency = ps.cpu_freq()[2]
        cpu_number = ps.cpu_count()
        pid_number = len(ps.pids())
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        temp = {'time':now,'cpu_perc':data,'host_nm':hostname,'total_ram':tot_mem,'used_ram':used_mem,'perc_used_ram':perc_mem,'cpu_speed':cpu_frequency,'cpu_no':cpu_number,'pid_no': pid_number}
    jsonstr=json.dumps(temp)
    return jsonstr 

if __name__ == '__main__':
	app.run(debug=False,port=5000,host=ip_addr)

from flask import Flask, render_template, request
import ipaddress

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    ip = request.form['ip']
    mask = request.form['mask']
    
    try:
        network = ipaddress.IPv4Network(f'{ip}/{mask}', strict=False)
        net_ip = network.network_address
        broadcast_ip = network.broadcast_address
        num_hosts = network.num_addresses - 2 
        host_range = f'{list(network.hosts())[0]} - {list(network.hosts())[-1]}'
        
        ip_class = determinar_ip_class(ip)
        ip_type = "Privada" if network.is_private else "Pública"
        
        net_bin = ''.join(f'{int(octet):08b}' for octet in str(net_ip).split('.'))
        host_bin = ''.join(f'{int(octet):08b}' for octet in str(broadcast_ip).split('.'))

        binario_completo = ''.join(f'{int(octet):08b}' for octet in ip.split('.'))
        longitud_red = network.prefixlen
        porcion_red = binario_completo[:longitud_red]
        porcion_host = binario_completo[longitud_red:]

        return render_template('result.html', net_ip=net_ip, broadcast_ip=broadcast_ip, 
                               num_hosts=num_hosts, host_range=host_range, ip_class=ip_class, 
                               ip_type=ip_type, porcion_red=porcion_red, porcion_host=porcion_host)
    except ValueError:
        return "Error: IP o máscara inválida."

def determinar_ip_class(ip):
    primer_octeto = int(ip.split('.')[0])
    if 1 <= primer_octeto <= 126:
        return 'Clase A'
    elif 128 <= primer_octeto <= 191:
        return 'Clase B'
    elif 192 <= primer_octeto <= 223:
        return 'Clase C'
    elif 224 <= primer_octeto <= 239:
        return 'Clase D (Multicast)'
    else:
        return 'Clase E (Reservada)'

if __name__ == '__main__':
    app.run(port=80)

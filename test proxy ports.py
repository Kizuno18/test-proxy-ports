import socket
from concurrent.futures import ThreadPoolExecutor
import os

def test_proxy(proxy):
    proxy = proxy.strip()  # remove espaços em branco no início e no fim
    if ":" not in proxy:
        return None  # ignora proxies inválidos que não contêm porta

    host, port = proxy.split(":")
    port = int(port)

    try:
        # Testa a conexão com as portas 7171 e 7272
        connected_ports = []
        for p in [7171, 7272]:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)  # define timeout de 5 segundos
                s.connect((host, p))
                connected_ports.append(p)

        if len(connected_ports) == 2:
            print(f"Proxy {proxy} está funcionando nas portas {connected_ports}")
            return proxy
        else:
            return None
    except:
        return None


def main(filename, output_file):
    if not os.path.isfile(filename):
        print(f"Arquivo de entrada {filename} não existe")
        return

    with open(filename, "r") as f:
        proxies = f.readlines()

    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(test_proxy, proxies)

    ips = [r for r in results if r is not None]

    # Salva os IPs em um arquivo de texto
    try:
        with open(output_file, "w") as f:
            for ip in ips:
                f.write(ip + "\n")
    except Exception as e:
        print(f"Erro ao escrever no arquivo de saída: {e}")
        return

    print(f"{len(ips)} proxies conectados foram salvos em {output_file}")


if __name__ == "__main__":
    main("prx.txt", "ips_conectados.txt")

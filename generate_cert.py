import os
import redfish
from dotenv import load_dotenv
from generate_csr import generate_csr
from import_ssl import import_ssl

if __name__ == "__main__":
    load_dotenv()

    ilo_host = os.environ["ILO_HOST"]
    ilo_username = os.environ["ILO_USERNAME"]
    ilo_password = os.environ["ILO_PASSWORD"]

    REST_OBJ = redfish.RedfishClient(
        base_url=ilo_host, username=ilo_username, password=ilo_password
    )
    REST_OBJ.login(auth="session")

    CSR_DICT = {
        "City": os.environ["CSR_CITY"],
        "CommonName": os.environ["CSR_CN"],
        "Country": os.environ["CSR_COUNTRY"],
        "OrgName": os.environ["CSR_ORGNAME"],
        "OrgUnit": os.environ["CSR_OU"],
        "State": os.environ["CSR_STATE"],
    }

    generate_csr(REST_OBJ, "output.csr", CSR_DICT)
    print("Requesting certificate from LetsEncrypt...")
    os.system(
        f"certbot certonly --csr ./output.csr --preferred-challenges dns --non-interactive --agree-tos -m {os.environ['CERT_EMAIL']} --dns-cloudflare --dns-cloudflare-credentials ./cloudflare-token.ini --config-dir ./config --work-dir ./work --logs-dir ./logs -d {os.environ['CSR_CN']}"
    )

    with open("./0000_cert.pem", "r") as cert_data:
        ssl_cert = cert_data.read()
        cert_data.close()

    import_ssl(REST_OBJ, ssl_cert)

    REST_OBJ.logout()

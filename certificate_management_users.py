from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
import os
from transitions import print_slow
import cipher

class ManageCertificates:
    def __init__(self, user):
        self.user = user
        self.solicitudes_folder = "AC1/solicitudes"

        os.makedirs(self.solicitudes_folder, exist_ok=True)

    def generate_certificate_request(self, user_private_key):

        csr = x509.CertificateSigningRequestBuilder().subject_name(
            x509.Name([
                x509.NameAttribute(NameOID.COMMON_NAME, str(self.user.id)),
                x509.NameAttribute(NameOID.SURNAME, self.user.second_name),
                x509.NameAttribute(NameOID.GIVEN_NAME, self.user.name),
                x509.NameAttribute(NameOID.EMAIL_ADDRESS, self.user.email),
            ])
        ).sign(user_private_key, hashes.SHA256(), default_backend())

        csr_filename = os.path.join(self.solicitudes_folder, f"{self.user.id}_request.pem")
        with open(csr_filename, 'wb') as csr_file:
            csr_file.write(csr.public_bytes(encoding=serialization.Encoding.PEM))

        return csr_filename

    def check_user_is_certified(self):
        # Ruta de la solicitud en la carpeta de solicitudes
        request_filename = os.path.join(self.solicitudes_folder, f"{self.user.id}_request.pem")

        # Verify if the application exists
        if os.path.exists(request_filename):
            print_slow("Currently, you don't possess a valid certification. Please try again at another time.")
            return False

        return True

"""
Script to generate self-signed SSL certificate for HTTPS
Run this once: python generate_cert.py
"""

import os
import subprocess
import sys

def generate_self_signed_cert():
    """Generate a self-signed SSL certificate"""
    
    cert_file = 'cert.pem'
    key_file = 'key.pem'
    
    # Check if certificates already exist
    if os.path.exists(cert_file) and os.path.exists(key_file):
        print(f"✓ Certificate files already exist: {cert_file}, {key_file}")
        return True
    
    print("Generating self-signed SSL certificate...")
    
    try:
        # Generate self-signed certificate using openssl
        command = [
            'openssl', 'req', '-x509', '-newkey', 'rsa:4096',
            '-nodes', '-out', cert_file, '-keyout', key_file,
            '-days', '365',
            '-subj', '/C=FR/ST=State/L=City/O=Organization/CN=localhost'
        ]
        
        subprocess.run(command, check=True, capture_output=True)
        print(f"✓ Certificate generated successfully!")
        print(f"  - Certificate: {cert_file}")
        print(f"  - Key: {key_file}")
        return True
        
    except FileNotFoundError:
        print("✗ OpenSSL not found. Trying alternative method...")
        try:
            generate_with_cryptography(cert_file, key_file)
            return True
        except Exception as e:
            print(f"✗ Failed to generate certificate: {e}")
            print("\nPlease install pyOpenSSL or OpenSSL:")
            print("  pip install pyopenssl")
            return False
    except Exception as e:
        print(f"✗ Error generating certificate: {e}")
        return False

def generate_with_cryptography(cert_file, key_file):
    """Alternative certificate generation using cryptography library"""
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization
    import datetime
    
    print("Using cryptography library...")
    
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
    )
    
    # Build certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"FR"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"State"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"City"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Organization"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
        critical=False,
    ).sign(private_key, hashes.SHA256())
    
    # Write certificate to file
    with open(cert_file, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    # Write key to file
    with open(key_file, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))
    
    print(f"✓ Certificate generated successfully with cryptography library!")
    print(f"  - Certificate: {cert_file}")
    print(f"  - Key: {key_file}")

if __name__ == '__main__':
    success = generate_self_signed_cert()
    sys.exit(0 if success else 1)

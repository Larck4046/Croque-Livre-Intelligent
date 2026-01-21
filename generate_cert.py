#!/usr/bin/env python3
"""
Generate self-signed SSL certificates for local HTTPS development
"""

import os
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta
import ipaddress

def generate_self_signed_cert():
    """Generate a self-signed certificate for localhost"""
    
    # Generate private key
    print("📝 Generating private key...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Generate certificate
    print("📝 Generating certificate...")
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
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName(u"localhost"),
            x509.DNSName(u"127.0.0.1"),
            x509.IPAddress(ipaddress.IPv4Address(u"127.0.0.1")),
        ]),
        critical=False,
    ).sign(private_key, hashes.SHA256(), default_backend())
    
    # Write certificate to file
    print("💾 Writing certificate to cert.pem...")
    with open("cert.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    # Write private key to file
    print("💾 Writing private key to key.pem...")
    with open("key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    print("\n✅ SSL certificates generated successfully!")
    print("   - cert.pem")
    print("   - key.pem")
    print("\n📝 Certificate details:")
    print(f"   - Subject: {cert.subject}")
    print(f"   - Issuer: {cert.issuer}")
    print(f"   - Valid from: {cert.not_valid_before}")
    print(f"   - Valid until: {cert.not_valid_after}")
    print("\n🚀 You can now run: python main_script.py")

if __name__ == "__main__":
    # Check if certificates already exist
    if os.path.exists("cert.pem") and os.path.exists("key.pem"):
        response = input("⚠️  Certificate files already exist. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled.")
            exit(0)
    
    try:
        generate_self_signed_cert()
    except ImportError:
        print("❌ Error: cryptography library not found")
        print("   Install it with: pip install cryptography")
        exit(1)
    except Exception as e:
        print(f"❌ Error generating certificate: {e}")
        exit(1)

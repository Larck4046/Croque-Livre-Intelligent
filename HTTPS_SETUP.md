# HTTPS Setup Instructions

## Quick Start

### 1. Generate SSL Certificate (Run once)

```bash
python generate_cert.py
```

This will create two files:
- `cert.pem` - SSL certificate
- `key.pem` - Private key

### 2. Install Required Packages

```bash
pip install flask pyopenssl
```

### 3. Start the Flask Server

```bash
python main_script.py
```

You should see:
```
✓ Starting Flask with HTTPS...
  Access the app at: https://localhost:5000
  (You may see a security warning - this is normal for self-signed certificates)
```

### 4. Access the App

Open your browser and go to: `https://localhost:5000`

**Note:** You may see a security warning because the certificate is self-signed. This is normal and safe for development. Click "Advanced" and then "Proceed" (or similar option depending on your browser).

## Why HTTPS is Required

The camera scanner feature (getUserMedia API) requires HTTPS or localhost to work. Now that your Flask app runs on HTTPS, the camera functionality will work properly.

## Troubleshooting

### "Certificate files not found" error
- Run `python generate_cert.py` first

### "OpenSSL not found" during certificate generation
- Install pyOpenSSL: `pip install pyopenssl`
- Or install OpenSSL separately

### Browser security warning
- This is normal for self-signed certificates used in development
- You can safely click through the warning

### Camera still not working
- Make sure you're using `https://localhost:5000` (with https)
- Check browser permissions for camera access
- Try a different browser (Chrome, Firefox, Edge)

## For Production

For production use, you should obtain a real SSL certificate from a Certificate Authority (Let's Encrypt, etc.) rather than using self-signed certificates.

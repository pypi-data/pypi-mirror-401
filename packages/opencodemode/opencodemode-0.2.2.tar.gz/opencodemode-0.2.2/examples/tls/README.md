# TLS/mTLS Example

This example demonstrates how to configure and use TLS encryption for secure gRPC communication in Codemode.

## Overview

TLS (Transport Layer Security) encrypts gRPC traffic between the main application and the executor sidecar, protecting against:
- Eavesdropping
- Man-in-the-middle (MITM) attacks
- Unauthorized access

## Quick Start

### 1. Generate Test Certificates

```bash
# From the repository root
make generate-certs

# Or manually
bash scripts/generate_test_certs.sh
```

This creates a `test_certs` directory with:
- `ca.crt` / `ca.key` - Certificate Authority
- `server.crt` / `server.key` - Server certificate
- `client.crt` / `client.key` - Client certificate (for mTLS)

### 2. Set Environment Variables

```bash
# Required
export CODEMODE_API_KEY=your-secure-api-key

# TLS configuration
export CODEMODE_GRPC_TLS_ENABLED=true
export CODEMODE_GRPC_TLS_MODE=custom
export CODEMODE_GRPC_TLS_CERT_FILE=./test_certs/server.crt
export CODEMODE_GRPC_TLS_KEY_FILE=./test_certs/server.key
export CODEMODE_GRPC_TLS_CA_FILE=./test_certs/ca.crt

# Optional: For mutual TLS (mTLS)
export CODEMODE_GRPC_TLS_CLIENT_CERT_FILE=./test_certs/client.crt
export CODEMODE_GRPC_TLS_CLIENT_KEY_FILE=./test_certs/client.key
export CODEMODE_GRPC_TLS_REQUIRE_CLIENT_AUTH=true
```

### 3. Run with Docker Compose

```bash
# Copy certificate files
cp -r test_certs certs/

# Start services
docker-compose up
```

## Configuration Modes

### Mode 1: System Certificates

Uses the operating system's trusted certificate store:

```yaml
grpc:
  tls:
    enabled: true
    mode: system
```

Best for: Production with CA-signed certificates

### Mode 2: Custom Certificates

Uses provided certificate files:

```yaml
grpc:
  tls:
    enabled: true
    mode: custom
    cert_file: ./certs/server.crt
    key_file: ./certs/server.key
    ca_file: ./certs/ca.crt
```

Best for: Development, testing, or internal CA

### Mode 3: Mutual TLS (mTLS)

Requires both server and client certificates:

```yaml
grpc:
  tls:
    enabled: true
    mode: custom
    cert_file: ./certs/server.crt
    key_file: ./certs/server.key
    ca_file: ./certs/ca.crt
    client_cert_file: ./certs/client.crt
    client_key_file: ./certs/client.key
```

Best for: Zero-trust environments, high-security requirements

## Testing

### Test TLS Server

```bash
# Terminal 1: Start ToolService with TLS
CODEMODE_GRPC_TLS_ENABLED=true \
CODEMODE_GRPC_TLS_MODE=custom \
CODEMODE_GRPC_TLS_CERT_FILE=./test_certs/server.crt \
CODEMODE_GRPC_TLS_KEY_FILE=./test_certs/server.key \
CODEMODE_GRPC_TLS_CA_FILE=./test_certs/ca.crt \
uv run python scripts/e2e_demo_toolservice_async.py

# Terminal 2: Start executor with TLS
docker run --rm \
  -e CODEMODE_GRPC_TLS_ENABLED=true \
  -e CODEMODE_GRPC_TLS_MODE=custom \
  -e CODEMODE_GRPC_TLS_CA_FILE=/certs/ca.crt \
  -e CODEMODE_API_KEY=dev-secret-key \
  -e MAIN_APP_GRPC_TARGET=host.docker.internal:50051 \
  -v $(pwd)/test_certs:/certs:ro \
  -p 8001:8001 \
  codemode-executor:0.1.0

# Terminal 3: Run driver
CODEMODE_API_KEY=dev-secret-key \
uv run python scripts/e2e_demo_driver_async.py
```

## Production Deployment

For production environments:

1. **Use CA-signed certificates** (e.g., Let's Encrypt, internal CA)
2. **Enable mTLS** for mutual authentication
3. **Rotate certificates** regularly
4. **Monitor certificate expiration**
5. **Use secrets management** (Kubernetes Secrets, Vault, etc.)
6. **Test in staging** first

### Production Certificate Example

```bash
# Get Let's Encrypt certificate
certbot certonly --standalone -d your-domain.com

# Configure Codemode
export CODEMODE_GRPC_TLS_CERT_FILE=/etc/letsencrypt/live/your-domain.com/fullchain.pem
export CODEMODE_GRPC_TLS_KEY_FILE=/etc/letsencrypt/live/your-domain.com/privkey.pem
```

## Troubleshooting

### Certificate Verification Failed

**Error:** `SSL certificate verify failed`

**Solution:**
- Ensure certificate CN/SAN matches the hostname
- Check certificate hasn't expired: `openssl x509 -in server.crt -noout -dates`
- Verify CA certificate is correct

### Connection Refused

**Error:** `Connection refused` or `UNAVAILABLE`

**Solution:**
- Check TLS is enabled on both client and server
- Verify certificate files exist and are readable
- Check firewall/network connectivity

### Invalid Certificate

**Error:** `certificate signed by unknown authority`

**Solution:**
- Provide CA certificate via `ca_file` or `CODEMODE_GRPC_TLS_CA_FILE`
- Ensure CA certificate is valid

## Security Best Practices

1. ✅ **Never commit private keys** to version control
2. ✅ **Use strong key sizes** (4096-bit RSA minimum)
3. ✅ **Set restrictive file permissions** (`chmod 600` for private keys)
4. ✅ **Enable mTLS** for production
5. ✅ **Rotate certificates** every 90 days
6. ✅ **Monitor certificate expiration**
7. ✅ **Use secrets management** tools
8. ✅ **Test certificate validation** in staging

## Performance

TLS adds approximately:
- **5-10% latency** per gRPC call
- **50-100ms** initial handshake
- **<5% CPU overhead** (with AES-NI)

The sidecar pattern (localhost communication) minimizes the impact.

## References

- [Codemode Documentation](../../README.md)
- [gRPC Security Guide](https://grpc.io/docs/guides/auth/)
- [OpenSSL Documentation](https://www.openssl.org/docs/)

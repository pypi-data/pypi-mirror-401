#!/bin/bash
# Generate self-signed certificates for testing TLS in Codemode

set -e

CERT_DIR="${1:-./test_certs}"
mkdir -p "$CERT_DIR"

echo "🔐 Generating test certificates in $CERT_DIR"
echo ""

# Generate CA
echo "📝 Generating Certificate Authority (CA)..."
openssl req -x509 -newkey rsa:4096 -days 365 -nodes \
  -keyout "$CERT_DIR/ca.key" \
  -out "$CERT_DIR/ca.crt" \
  -subj "/CN=Test CA/O=Codemode Test" \
  2>/dev/null

echo "   ✓ CA certificate: $CERT_DIR/ca.crt"
echo "   ✓ CA key: $CERT_DIR/ca.key"
echo ""

# Generate server certificate
echo "📝 Generating server certificate..."
openssl req -newkey rsa:4096 -nodes \
  -keyout "$CERT_DIR/server.key" \
  -out "$CERT_DIR/server.csr" \
  -subj "/CN=localhost/O=Codemode Test" \
  2>/dev/null

openssl x509 -req -in "$CERT_DIR/server.csr" \
  -CA "$CERT_DIR/ca.crt" \
  -CAkey "$CERT_DIR/ca.key" \
  -CAcreateserial \
  -out "$CERT_DIR/server.crt" \
  -days 365 \
  -extfile <(echo "subjectAltName=DNS:localhost,DNS:executor,DNS:host.docker.internal,IP:127.0.0.1") \
  2>/dev/null

rm "$CERT_DIR/server.csr"

echo "   ✓ Server certificate: $CERT_DIR/server.crt"
echo "   ✓ Server key: $CERT_DIR/server.key"
echo ""

# Generate client certificate (for mTLS)
echo "📝 Generating client certificate for mTLS..."
openssl req -newkey rsa:4096 -nodes \
  -keyout "$CERT_DIR/client.key" \
  -out "$CERT_DIR/client.csr" \
  -subj "/CN=client/O=Codemode Test" \
  2>/dev/null

openssl x509 -req -in "$CERT_DIR/client.csr" \
  -CA "$CERT_DIR/ca.crt" \
  -CAkey "$CERT_DIR/ca.key" \
  -CAcreateserial \
  -out "$CERT_DIR/client.crt" \
  -days 365 \
  2>/dev/null

rm "$CERT_DIR/client.csr"

echo "   ✓ Client certificate: $CERT_DIR/client.crt"
echo "   ✓ Client key: $CERT_DIR/client.key"
echo ""

# Set appropriate permissions
chmod 600 "$CERT_DIR"/*.key
chmod 644 "$CERT_DIR"/*.crt

echo "✅ Test certificates generated successfully!"
echo ""
echo "📋 Summary:"
ls -lh "$CERT_DIR"
echo ""
echo "🔧 Usage:"
echo "   Set environment variables:"
echo "   export CODEMODE_GRPC_TLS_ENABLED=true"
echo "   export CODEMODE_GRPC_TLS_MODE=custom"
echo "   export CODEMODE_GRPC_TLS_CERT_FILE=$CERT_DIR/server.crt"
echo "   export CODEMODE_GRPC_TLS_KEY_FILE=$CERT_DIR/server.key"
echo "   export CODEMODE_GRPC_TLS_CA_FILE=$CERT_DIR/ca.crt"
echo ""
echo "   For mTLS, also set:"
echo "   export CODEMODE_GRPC_TLS_CLIENT_CERT_FILE=$CERT_DIR/client.crt"
echo "   export CODEMODE_GRPC_TLS_CLIENT_KEY_FILE=$CERT_DIR/client.key"
echo "   export CODEMODE_GRPC_TLS_REQUIRE_CLIENT_AUTH=true"

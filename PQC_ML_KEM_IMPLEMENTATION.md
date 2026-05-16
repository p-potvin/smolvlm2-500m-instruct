# Post-Quantum Cryptography (PQC) and ML-KEM Implementation

## Overview
This document outlines the architecture, requirements, and steps for implementing Module-Lattice-Based Key-Encapsulation Mechanism (ML-KEM, formerly known as CRYSTALS-Kyber) for "serverless" encryption within the VaultWares project. As quantum computing advances, traditional public-key cryptography (like RSA and ECC) becomes vulnerable. ML-KEM provides a quantum-resistant key encapsulation mechanism standardized by NIST (FIPS 203).

## Architecture
The ML-KEM implementation will be integrated into the serverless backend (Google Cloud Run/Functions and Azure equivalents) to ensure secure key exchange between the client (Vault Player / Frontend) and the API server.

### Key Components
1. **Client-Side (Vault Player / Frontend)**:
   - Generates an ML-KEM public/private key pair.
   - Transmits the public key to the serverless endpoint over TLS.
2. **Serverless Backend (API Server)**:
   - Receives the client's ML-KEM public key.
   - Generates a shared secret and encapsulates it using the client's public key (producing ciphertext).
   - Sends the ciphertext back to the client.
3. **Symmetric Encryption**:
   - The client decapsulates the ciphertext using its private key to derive the shared secret.
   - Both parties use the shared secret with AES-256-GCM for encrypting subsequent payloads.

## Requirements
- **Dependencies**:
  - Python: `cryptography` library (when PQC support is fully integrated) or a specialized library like `liboqs-python` or `pycryptodome` (with Kyber support).
  - Node.js (Frontend): WebAssembly compiled `liboqs` or an equivalent JS ML-KEM implementation.
- **Environment**: Serverless functions must have sufficient memory and timeout limits, as lattice-based cryptography can have larger key sizes (e.g., 800 bytes to 1.5 KB for ML-KEM-512/768) compared to ECC.
- **Backward Compatibility**: Implement a hybrid scheme combining ML-KEM with X25519 (ECDHE) to ensure security even if the ML-KEM implementation has unforeseen vulnerabilities.

## Implementation Steps

### Phase 1: Dependency Setup
1. Add the appropriate PQC library to `requirements.txt` for the Python backend.
   ```text
   # Example: liboqs-python for testing
   liboqs-python==X.Y.Z
   ```

### Phase 2: Hybrid Key Encapsulation Endpoint
1. Create a new authentication endpoint (e.g., `/auth/kem-exchange`) in `api_server.py`.
2. The endpoint should accept the client's hybrid public key (X25519 + ML-KEM-768).
3. The server generates the shared secret, encapsulates it, and returns the ciphertext.

### Phase 3: Middleware Integration
1. Update the `gate_requests` middleware to decrypt incoming encrypted payloads using the established symmetric shared secret.
2. Encrypt outgoing responses using the same shared secret.

## Security Considerations
- **Key Sizes**: ML-KEM public keys and ciphertexts are larger than classical ones. Ensure the serverless API gateway (e.g., Nginx, Cloud Load Balancer) does not drop large headers if keys are passed there.
- **Replay Attacks**: Always use nonces/IVs in the subsequent symmetric encryption phase to prevent replay attacks.
- **Hybrid Approach**: NIST recommends using a hybrid approach (Classical + PQC) during the transition period. Do not rely solely on ML-KEM yet.

## Future Work
- Monitor NIST updates on FIPS 203.
- Integrate ML-KEM directly into the database connection logic (e.g., PostgreSQL TLS connections with PQC algorithms).

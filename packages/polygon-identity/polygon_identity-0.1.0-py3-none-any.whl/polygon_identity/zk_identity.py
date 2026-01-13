from nacl.hash import blake2b
from nacl.encoding import HexEncoder
from typing import Dict

class ZKProof:
    """Zero-knowledge proof data structure.
    
    Args:
        commitment: Hash commitment of the proof
        proof: The proof data
    """
    def __init__(self, commitment: str, proof: str):
        self.commitment = commitment
        self.proof = proof

class ZKIdentity:
    """Zero-knowledge identity utilities for generating and verifying proofs.
    
    This class provides methods for creating commitments and proofs without
    revealing the original secret data.
    """
    def generate_commitment(self, data: str) -> str:
        """Generate a commitment hash from data.
        
        Args:
            data: Data to create commitment for
            
        Returns:
            Hex-encoded commitment hash
        """
        data_bytes = data.encode('utf-8')
        hash_bytes = blake2b(data_bytes, encoder=HexEncoder, digest_size=64)
        return hash_bytes.decode('utf-8')

    def generate_proof(self, secret: str, public_data: str) -> ZKProof:
        """Generate a zero-knowledge proof.
        
        Args:
            secret: Secret data to prove knowledge of
            public_data: Public data to include in proof
            
        Returns:
            ZKProof object containing commitment and proof
        """
        commitment = self.generate_commitment(secret + public_data)
        proof_data = (secret + public_data + commitment).encode('utf-8')
        proof = blake2b(proof_data, encoder=HexEncoder, digest_size=64).decode('utf-8')

        return ZKProof(commitment=commitment, proof=proof)

    def verify_proof(self, proof: ZKProof, public_data: str) -> bool:
        """Verify a zero-knowledge proof.
        
        Args:
            proof: ZKProof object to verify
            public_data: Public data used in proof generation
            
        Returns:
            True if proof is valid, False otherwise
        """
        proof_data = (proof.proof + public_data).encode('utf-8')
        expected_commitment = blake2b(proof_data, encoder=HexEncoder, digest_size=64).decode('utf-8')
        return expected_commitment == proof.commitment


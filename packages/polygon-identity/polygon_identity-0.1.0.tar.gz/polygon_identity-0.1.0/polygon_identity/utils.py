"""Utility functions for polygon-identity package."""

from typing import List, Tuple
from web3 import Web3


def validate_address(address: str) -> bool:
    """Validate an Ethereum address.
    
    Args:
        address: Address to validate
        
    Returns:
        True if valid address format
    """
    if not address or not isinstance(address, str):
        return False
    
    if not address.startswith('0x'):
        return False
    
    if len(address) != 42:
        return False
    
    try:
        Web3.to_checksum_address(address)
        return True
    except (ValueError, TypeError):
        return False


def validate_guardians(guardians: List[str], threshold: int) -> Tuple[bool, str]:
    """Validate guardian configuration.
    
    Args:
        guardians: List of guardian addresses
        threshold: Required approval threshold
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not guardians:
        return False, "At least one guardian is required"
    
    if threshold <= 0:
        return False, "Threshold must be greater than 0"
    
    if threshold > len(guardians):
        return False, f"Threshold ({threshold}) cannot exceed number of guardians ({len(guardians)})"
    
    for guardian in guardians:
        if not validate_address(guardian):
            return False, f"Invalid guardian address: {guardian}"
    
    if len(guardians) != len(set(guardians)):
        return False, "Duplicate guardians not allowed"
    
    return True, ""


def format_identity_data(identity_data: tuple) -> dict:
    """Format raw identity data from contract into a dictionary.
    
    Args:
        identity_data: Tuple from contract (owner, public_key, created_at, is_active)
        
    Returns:
        Formatted dictionary
    """
    return {
        'owner': identity_data[0],
        'public_key': identity_data[1],
        'created_at': identity_data[2],
        'is_active': identity_data[3]
    }


def check_sufficient_gas(w3: Web3, transaction: dict, buffer_multiplier: float = 1.2) -> bool:
    """Check if account has sufficient gas for transaction.
    
    Args:
        w3: Web3 instance
        transaction: Transaction dictionary
        buffer_multiplier: Safety buffer (default 1.2 = 20% extra)
        
    Returns:
        True if sufficient gas available
    """
    try:
        estimated_gas = w3.eth.estimate_gas(transaction)
        gas_price = transaction.get('gasPrice', w3.eth.gas_price)
        
        required_gas = int(estimated_gas * buffer_multiplier)
        cost = required_gas * gas_price
        
        balance = w3.eth.get_balance(transaction['from'])
        
        return balance >= cost
    except (ValueError, AttributeError, KeyError):
        return False


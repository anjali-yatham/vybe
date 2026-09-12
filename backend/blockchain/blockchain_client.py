"""
Blockchain client for interacting with the TicketOwnership smart contract on Polygon Amoy.
"""
import os
import json
from pathlib import Path
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from dotenv import load_dotenv

# Load environment variables from blockchain/.env (for ALCHEMY_API_KEY and PRIVATE_KEY)
blockchain_env_path = Path(__file__).parent / '.env'
load_dotenv(blockchain_env_path)

# Load environment variables from backend/.env (for TICKET_OWNERSHIP_CONTRACT_ADDRESS)
# Use override=True to ensure values from backend/.env take precedence
backend_env_path = Path(__file__).parent.parent / '.env'
load_dotenv(backend_env_path, override=True)

# Environment variables
ALCHEMY_API_KEY = os.getenv('ALCHEMY_API_KEY')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
TICKET_OWNERSHIP_CONTRACT_ADDRESS = os.getenv('TICKET_OWNERSHIP_CONTRACT_ADDRESS')

# Polygon Amoy RPC URL
POLYGON_AMOY_RPC = f"https://polygon-amoy.g.alchemy.com/v2/{ALCHEMY_API_KEY}"

# Load contract ABI
ABI_PATH = Path(__file__).parent / 'ignition' / 'deployments' / 'chain-80002' / 'artifacts' / 'TicketOwnershipModule#TicketOwnership.json'

def load_contract_abi():
    """Load the contract ABI from the deployment artifacts."""
    with open(ABI_PATH, 'r') as f:
        contract_json = json.load(f)
        return contract_json['abi']

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(POLYGON_AMOY_RPC))

# Add PoA middleware for Polygon Amoy (required for proof-of-authority chains)
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

# Load contract
contract_abi = load_contract_abi()
contract = w3.eth.contract(
    address=Web3.to_checksum_address(TICKET_OWNERSHIP_CONTRACT_ADDRESS),
    abi=contract_abi
)

# Account from private key
account = w3.eth.account.from_key(PRIVATE_KEY)


def issue_ticket_onchain(ticket_id: str, owner_address: str) -> str:
    """
    Issue a ticket on the blockchain.
    
    Args:
        ticket_id: Unique identifier for the ticket
        owner_address: Ethereum address of the ticket owner
        
    Returns:
        Transaction hash as a hex string
    """
    # Validate connection
    if not w3.is_connected():
        raise ConnectionError("Failed to connect to Polygon Amoy network")
    
    # Ensure address is checksummed
    owner_address = Web3.to_checksum_address(owner_address)
    
    # Build transaction
    nonce = w3.eth.get_transaction_count(account.address)
    
    # Estimate gas
    gas_estimate = contract.functions.issueTicket(
        ticket_id,
        owner_address
    ).estimate_gas({'from': account.address})
    
    # Build transaction
    transaction = contract.functions.issueTicket(
        ticket_id,
        owner_address
    ).build_transaction({
        'chainId': 80002,  # Polygon Amoy chain ID
        'gas': gas_estimate + 10000,  # Add buffer
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce,
        'from': account.address
    })
    
    # Sign transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
    
    # Send transaction
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    
    # Wait for transaction receipt
    print(f"Transaction sent. Hash: {tx_hash.hex()}")
    print("Waiting for confirmation...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    
    if tx_receipt['status'] == 1:
        print(f"✓ Transaction confirmed in block {tx_receipt['blockNumber']}")
    else:
        print("✗ Transaction failed")
        raise Exception(f"Transaction failed with receipt: {tx_receipt}")
    
    return tx_hash.hex()


def get_ticket_owner_onchain(ticket_id: str) -> dict:
    """
    Get the owner of a ticket from the blockchain (read-only call).
    
    Args:
        ticket_id: Unique identifier for the ticket
        
    Returns:
        Dictionary containing:
        - owner: Ethereum address of the ticket owner
        - isValid: Boolean indicating if the ticket is valid
    """
    # Validate connection
    if not w3.is_connected():
        raise ConnectionError("Failed to connect to Polygon Amoy network")
    
    # Call view function (no gas needed)
    result = contract.functions.getTicketOwner(ticket_id).call()
    
    return {
        'owner': result[0],
        'isValid': result[1]
    }


if __name__ == "__main__":
    """Test the blockchain client functions."""
    
    print("=" * 60)
    print("Blockchain Client Test")
    print("=" * 60)
    print(f"Connected to: Polygon Amoy")
    print(f"Contract Address: {TICKET_OWNERSHIP_CONTRACT_ADDRESS}")
    print(f"Account Address: {account.address}")
    print(f"Network Connected: {w3.is_connected()}")
    print("=" * 60)
    
    # Test parameters
    test_ticket_id = "TEST-001"
    test_owner_address = account.address  # Using the account's own address
    
    try:
        # Test 1: Issue a ticket
        print(f"\n[TEST 1] Issuing ticket '{test_ticket_id}' to {test_owner_address}")
        tx_hash = issue_ticket_onchain(test_ticket_id, test_owner_address)
        print(f"✓ Transaction Hash: {tx_hash}")
        
        # Test 2: Get ticket owner
        print(f"\n[TEST 2] Getting owner of ticket '{test_ticket_id}'")
        owner_info = get_ticket_owner_onchain(test_ticket_id)
        print(f"✓ Owner: {owner_info['owner']}")
        print(f"✓ Valid: {owner_info['isValid']}")
        
        # Verify the owner matches
        if owner_info['owner'].lower() == test_owner_address.lower():
            print(f"\n✓ SUCCESS: Ticket owner matches expected address!")
        else:
            print(f"\n✗ ERROR: Owner mismatch!")
            
    except Exception as e:
        print(f"\n✗ Error during testing: {str(e)}")
        raise
    
    print("\n" + "=" * 60)
    print("Test completed successfully!")
    print("=" * 60)

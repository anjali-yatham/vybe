// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title TicketOwnership
 * @dev A simple smart contract for managing ticket ownership on blockchain
 * @notice This is a student project demo, not for production use
 */
contract TicketOwnership {
    
    // Struct to represent a ticket with its ownership information
    struct Ticket {
        string ticketId;      // Unique identifier for the ticket
        address currentOwner; // Address of the current ticket owner
        bool isValid;         // Whether the ticket is currently valid
    }
    
    // Mapping from ticket ID to Ticket struct
    mapping(string => Ticket) private tickets;
    
    // Event emitted when a ticket is transferred to a new owner
    event TicketTransferred(
        string indexed ticketId,
        address indexed fromAddress,
        address indexed toAddress
    );
    
    /**
     * @dev Issue a new ticket to an owner
     * @param ticketId The unique identifier for the ticket
     * @param owner The address of the initial ticket owner
     */
    function issueTicket(string memory ticketId, address owner) public {
        // Create a new ticket with isValid = true
        tickets[ticketId] = Ticket({
            ticketId: ticketId,
            currentOwner: owner,
            isValid: true
        });
        
        // Emit transfer event (from zero address to owner)
        emit TicketTransferred(ticketId, address(0), owner);
    }
    
    /**
     * @dev Transfer a ticket to a new owner
     * @param ticketId The unique identifier of the ticket to transfer
     * @param newOwner The address of the new ticket owner
     * @notice Only works if the ticket exists and isValid is true
     */
    function transferTicket(string memory ticketId, address newOwner) public {
        Ticket storage ticket = tickets[ticketId];
        
        // Check that the ticket exists (has been issued)
        require(ticket.currentOwner != address(0), "Ticket does not exist");
        
        // Check that the ticket is still valid
        require(ticket.isValid, "Ticket is not valid");
        
        // Store the old owner for the event
        address oldOwner = ticket.currentOwner;
        
        // Transfer ownership to the new owner
        ticket.currentOwner = newOwner;
        // Keep isValid = true after transfer
        
        // Emit transfer event
        emit TicketTransferred(ticketId, oldOwner, newOwner);
    }
    
    /**
     * @dev Revoke a ticket, making it invalid
     * @param ticketId The unique identifier of the ticket to revoke
     * @notice Used when a ticket is resold, so the old record becomes invalid
     */
    function revokeTicket(string memory ticketId) public {
        Ticket storage ticket = tickets[ticketId];
        
        // Check that the ticket exists
        require(ticket.currentOwner != address(0), "Ticket does not exist");
        
        // Set isValid to false
        ticket.isValid = false;
    }
    
    /**
     * @dev Get the current owner and validity status of a ticket
     * @param ticketId The unique identifier of the ticket to query
     * @return owner The address of the current ticket owner
     * @return isValid Whether the ticket is currently valid
     */
    function getTicketOwner(string memory ticketId) public view returns (address owner, bool isValid) {
        Ticket storage ticket = tickets[ticketId];
        return (ticket.currentOwner, ticket.isValid);
    }
}

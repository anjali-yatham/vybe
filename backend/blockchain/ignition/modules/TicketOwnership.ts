import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

export default buildModule("TicketOwnershipModule", (m) => {
  const ticketOwnership = m.contract("TicketOwnership");

  return { ticketOwnership };
});

import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Landing from './pages/Landing'
import Login from './pages/Login'
import Signup from './pages/Signup'
import UserDashboard from './pages/UserDashboard'
import AdminDashboard from './pages/AdminDashboard'
import DashboardLayout from './components/DashboardLayout'
import BuyTickets from './pages/BuyTickets'
import ResellTicket from './pages/ResellTicket'
import Marketplace from './pages/Marketplace'
import TrustScore from './pages/TrustScore'
import TransactionHistory from './pages/TransactionHistory'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        
        {/* Dashboard with nested routes */}
        <Route path="/dashboard" element={<DashboardLayout />}>
          <Route index element={<UserDashboard />} />
          <Route path="buy" element={<BuyTickets />} />
          <Route path="resell" element={<ResellTicket />} />
          <Route path="marketplace" element={<Marketplace />} />
          <Route path="trust-score" element={<TrustScore />} />
          <Route path="history" element={<TransactionHistory />} />
        </Route>
        
        <Route path="/admin" element={<AdminDashboard />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App

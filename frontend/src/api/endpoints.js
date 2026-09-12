import { BASE_URL } from './config'

/**
 * Fetch all users from the backend
 * @returns {Promise<Array>} Array of user objects
 */
export async function getUsers() {
  try {
    const response = await fetch(`${BASE_URL}/users`)
    
    if (!response.ok) {
      throw new Error(`Failed to fetch users: ${response.status} ${response.statusText}`)
    }
    
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Error in getUsers():', error)
    throw error
  }
}

/**
 * Fetch all events from the backend
 * @returns {Promise<Array>} Array of event objects
 */
export async function getEvents() {
  try {
    const response = await fetch(`${BASE_URL}/events`)
    
    if (!response.ok) {
      throw new Error(`Failed to fetch events: ${response.status} ${response.statusText}`)
    }
    
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Error in getEvents():', error)
    throw error
  }
}

/**
 * Fetch all primary sales from the backend
 * @returns {Promise<Array>} Array of primary sale objects
 */
export async function getPrimarySales() {
  try {
    const response = await fetch(`${BASE_URL}/primary-sales`)
    
    if (!response.ok) {
      throw new Error(`Failed to fetch primary sales: ${response.status} ${response.statusText}`)
    }
    
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Error in getPrimarySales():', error)
    throw error
  }
}

/**
 * Fetch all resale transactions from the backend
 * @returns {Promise<Array>} Array of resale transaction objects
 */
export async function getResaleTransactions() {
  try {
    const response = await fetch(`${BASE_URL}/resale-transactions`)
    
    if (!response.ok) {
      throw new Error(`Failed to fetch resale transactions: ${response.status} ${response.statusText}`)
    }
    
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Error in getResaleTransactions():', error)
    throw error
  }
}

/**
 * Evaluate a transaction for fraud detection
 * @param {Object} transactionData - Transaction data to evaluate
 * @returns {Promise<Object>} Evaluation result with status, trust profile, and explanation
 */
export async function evaluateTransaction(transactionData) {
  try {
    const response = await fetch(`${BASE_URL}/evaluate-transaction`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(transactionData),
    })
    
    if (!response.ok) {
      throw new Error(`Failed to evaluate transaction: ${response.status} ${response.statusText}`)
    }
    
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Error in evaluateTransaction():', error)
    throw error
  }
}

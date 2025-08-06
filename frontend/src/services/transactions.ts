import axios from 'axios';

const API_URL = 'http://localhost:5000';

export interface Transaction {
  id?: number;
  asset_id: number;
  transaction_type: 'buy' | 'sell';
  quantity: number;
  unit_price: number;
  total_value?: number;
  transaction_date: string;
  description?: string;
  created_at?: string;
  updated_at?: string;
}

export interface TransactionSummary {
  current_quantity: number;
  current_value: number;
  average_cost: number;
  total_invested: number;
  total_divested: number;
  realized_gain_loss: number;
  unrealized_gain_loss: number;
  transaction_count: number;
}

export async function getTransactions(assetId?: number, familyId?: number) {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  const params: any = {};
  if (assetId) params.asset_id = assetId;
  if (familyId) params.family_id = familyId;

  const response = await axios.get(`${API_URL}/transactions`, {
    headers: {
      'Authorization': `Bearer ${token}`
    },
    params
  });
  
  return response.data;
}

export async function getTransaction(transactionId: number) {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  const response = await axios.get(`${API_URL}/transactions/${transactionId}`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return response.data;
}

export async function createTransaction(transaction: Omit<Transaction, 'id' | 'total_value' | 'created_at' | 'updated_at'>) {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  const response = await axios.post(`${API_URL}/transactions`, transaction, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  
  return response.data;
}

export async function updateTransaction(transactionId: number, transaction: Partial<Transaction>) {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  const response = await axios.put(`${API_URL}/transactions/${transactionId}`, transaction, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  
  return response.data;
}

export async function deleteTransaction(transactionId: number) {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  const response = await axios.delete(`${API_URL}/transactions/${transactionId}`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return response.data;
}

export async function getTransactionSummary(assetId: number): Promise<TransactionSummary> {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  const response = await axios.get(`${API_URL}/transactions/asset/${assetId}/summary`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return response.data;
}
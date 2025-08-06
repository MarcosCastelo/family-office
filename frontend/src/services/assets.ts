import axios from 'axios';

const API_URL = 'http://localhost:5000';

export interface Asset {
  id?: number;
  name: string;
  asset_type: string;
  value?: number; // Legacy field - now optional
  family_id: number;
  details?: any;
  // Dynamic calculated fields from transactions
  current_quantity?: number;
  current_value?: number;
  average_cost?: number;
  total_invested?: number;
  total_divested?: number;
  realized_gain_loss?: number;
  unrealized_gain_loss?: number;
  transaction_count?: number;
  acquisition_date?: string;
  created_at?: string;
}

export async function getAssets(familyId: number) {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  const response = await axios.get(`${API_URL}/assets`, {
    headers: {
      'Authorization': `Bearer ${token}`
    },
    params: {
      family_id: familyId
    }
  });
  
  return response.data;
}

export async function getAsset(assetId: number, familyId: number) {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  const response = await axios.get(`${API_URL}/assets/${assetId}`, {
    headers: {
      'Authorization': `Bearer ${token}`
    },
    params: {
      family_id: familyId
    }
  });
  
  return response.data;
}

export async function createAsset(asset: Asset) {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  const response = await axios.post(`${API_URL}/assets`, asset, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  
  return response.data;
}

export async function updateAsset(assetId: number, asset: Partial<Asset>, familyId: number) {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  const response = await axios.put(`${API_URL}/assets/${assetId}`, asset, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    params: {
      family_id: familyId
    }
  });
  
  return response.data;
}

export async function deleteAsset(assetId: number, familyId: number) {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  const response = await axios.delete(`${API_URL}/assets/${assetId}`, {
    headers: {
      'Authorization': `Bearer ${token}`
    },
    params: {
      family_id: familyId
    }
  });
  
  return response.data;
}

export async function uploadAssets(file: File, familyId: number) {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  const formData = new FormData();
  formData.append('file', file);

  const response = await axios.post(`${API_URL}/assets/upload`, formData, {
    headers: {
      'Authorization': `Bearer ${token}`
      // Removido Content-Type para deixar axios definir automaticamente
    },
    params: {
      family_id: familyId
    }
  });
  
  return response.data;
}

export async function uploadPdfAssets(file: File, familyId: number) {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  console.log('Service: Uploading PDF file:', file.name, 'size:', file.size);
  
  const formData = new FormData();
  formData.append('file', file);
  
  console.log('Service: FormData created, entries:', formData.entries());

  const response = await axios.post(`${API_URL}/assets/upload-pdf`, formData, {
    headers: {
      'Authorization': `Bearer ${token}`
      // Removido Content-Type para deixar axios definir automaticamente
    },
    params: {
      family_id: familyId
    }
  });
  
  console.log('Service: Upload response:', response.data);
  return response.data;
} 
import axios from 'axios';

const API_URL = 'http://localhost:5000';

export async function getDashboardData(familyId: number) {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  const response = await axios.get(`${API_URL}/dashboard`, {
    headers: {
      'Authorization': `Bearer ${token}`
    },
    params: {
      family_id: familyId
    }
  });
  
  return response.data;
} 
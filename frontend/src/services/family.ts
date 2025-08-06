import axios from 'axios';

const API_URL = 'http://localhost:5000';

export async function getUserFamilies() {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  const response = await axios.get(`${API_URL}/families`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return response.data;
} 
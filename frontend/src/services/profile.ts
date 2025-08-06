import axios from 'axios';

const API_URL = 'http://localhost:5000';

export interface UserProfile {
  id: number;
  email: string;
  active: boolean;
  families: Array<{
    id: number;
    name: string;
  }>;
  permissions: Array<{
    id: number;
    name: string;
  }>;
}

export async function getCurrentUser(): Promise<UserProfile> {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  const response = await axios.get(`${API_URL}/auth/me`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return response.data;
}

export async function updatePassword(currentPassword: string, newPassword: string): Promise<void> {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Token de acesso não encontrado');
  }

  await axios.put(`${API_URL}/auth/password`, {
    current_password: currentPassword,
    new_password: newPassword
  }, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
} 
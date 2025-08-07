import axios from 'axios';

const API_URL = 'http://localhost:5000';

// Helper para obter headers com token
const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
  return {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  };
};

// ===== ADMIN DASHBOARD =====

export async function getAdminDashboard() {
  const response = await axios.get(`${API_URL}/admin/dashboard`, {
    headers: getAuthHeaders()
  });
  return response.data;
}

// ===== USER MANAGEMENT =====

export interface User {
  id: number;
  email: string;
  active: boolean;
  families?: Array<{ id: number; name: string }>;
  permissions?: Array<{ id: number; name: string }>;
}

export async function getUsers(): Promise<User[]> {
  const response = await axios.get(`${API_URL}/admin/users`, {
    headers: getAuthHeaders()
  });
  return response.data;
}

export async function createUser(userData: { email: string; password: string; active?: boolean }): Promise<User> {
  const response = await axios.post(`${API_URL}/admin/users`, userData, {
    headers: getAuthHeaders()
  });
  return response.data;
}

export async function getUserDetails(userId: number): Promise<User> {
  const response = await axios.get(`${API_URL}/admin/users/${userId}`, {
    headers: getAuthHeaders()
  });
  return response.data;
}

export async function updateUser(userId: number, userData: { email?: string; password?: string; active?: boolean }): Promise<User> {
  const response = await axios.put(`${API_URL}/admin/users/${userId}`, userData, {
    headers: getAuthHeaders()
  });
  return response.data;
}

export async function deleteUser(userId: number): Promise<{ message: string }> {
  const response = await axios.delete(`${API_URL}/admin/users/${userId}`, {
    headers: getAuthHeaders()
  });
  return response.data;
}

// ===== FAMILY MANAGEMENT =====

export interface Family {
  id: number;
  name: string;
  user_count?: number;
}

export async function getFamilies(): Promise<Family[]> {
  const response = await axios.get(`${API_URL}/admin/families`, {
    headers: getAuthHeaders()
  });
  return response.data;
}

export async function createFamily(familyData: { name: string }): Promise<Family> {
  const response = await axios.post(`${API_URL}/admin/families`, familyData, {
    headers: getAuthHeaders()
  });
  return response.data;
}

export async function updateFamily(familyId: number, familyData: { name: string }): Promise<Family> {
  const response = await axios.put(`${API_URL}/admin/families/${familyId}`, familyData, {
    headers: getAuthHeaders()
  });
  return response.data;
}

export async function deleteFamily(familyId: number): Promise<{ message: string }> {
  const response = await axios.delete(`${API_URL}/admin/families/${familyId}`, {
    headers: getAuthHeaders()
  });
  return response.data;
}

export async function addUserToFamily(familyId: number, userId: number): Promise<{ message: string }> {
  const response = await axios.post(`${API_URL}/admin/families/${familyId}/add_user/${userId}`, {}, {
    headers: getAuthHeaders()
  });
  return response.data;
}

export async function removeUserFromFamily(familyId: number, userId: number): Promise<{ message: string }> {
  const response = await axios.post(`${API_URL}/admin/families/${familyId}/remove_user/${userId}`, {}, {
    headers: getAuthHeaders()
  });
  return response.data;
}

// ===== PERMISSION MANAGEMENT =====

export interface Permission {
  id: number;
  name: string;
  description?: string;
  user_count?: number;
}

export async function getPermissions(): Promise<Permission[]> {
  const response = await axios.get(`${API_URL}/admin/permissions`, {
    headers: getAuthHeaders()
  });
  return response.data;
}

export async function createPermission(permissionData: { name: string; description?: string }): Promise<Permission> {
  const response = await axios.post(`${API_URL}/admin/permissions`, permissionData, {
    headers: getAuthHeaders()
  });
  return response.data;
}

export async function updatePermission(permissionId: number, permissionData: { name?: string; description?: string }): Promise<Permission> {
  const response = await axios.put(`${API_URL}/admin/permissions/${permissionId}`, permissionData, {
    headers: getAuthHeaders()
  });
  return response.data;
}

export async function deletePermission(permissionId: number): Promise<{ message: string }> {
  const response = await axios.delete(`${API_URL}/admin/permissions/${permissionId}`, {
    headers: getAuthHeaders()
  });
  return response.data;
}

export async function addPermissionToUser(userId: number, permissionId: number): Promise<{ message: string }> {
  const response = await axios.post(`${API_URL}/admin/users/${userId}/permissions/${permissionId}`, {}, {
    headers: getAuthHeaders()
  });
  return response.data;
}

export async function removePermissionFromUser(userId: number, permissionId: number): Promise<{ message: string }> {
  const response = await axios.delete(`${API_URL}/admin/users/${userId}/permissions/${permissionId}`, {
    headers: getAuthHeaders()
  });
  return response.data;
} 
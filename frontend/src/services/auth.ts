import axios from 'axios';

const API_URL = 'http://localhost:5000';

// Criar instância do axios para auth
const authApi = axios.create({
  baseURL: API_URL,
  timeout: 10000
});

// Função para fazer login
export async function login(email: string, password: string) {
  const response = await authApi.post('/auth/login', {
    email,
    password
  });
  return response.data;
}

// Função para fazer refresh do token
export async function refreshToken(refreshToken: string) {
  try {
    const response = await authApi.post('/auth/refresh', {}, {
      headers: {
        'Authorization': `Bearer ${refreshToken}`
      }
    });
    return response.data;
  } catch (error) {
    throw error;
  }
}

// Função para fazer logout
export async function logout() {
  const token = localStorage.getItem('access_token');
  if (token) {
    try {
      await authApi.post('/auth/logout', {}, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
    } catch (error) {
      // Ignora erros no logout, pois o token pode já estar expirado
      console.log('Erro no logout do servidor (pode ser normal):', error);
    }
  }
}

// Configurar interceptor para requisições
export function setupAxiosInterceptors(onTokenExpired: () => void) {
  // Interceptor para requisições
  axios.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  // Interceptor para respostas
  axios.interceptors.response.use(
    (response) => {
      return response;
    },
    async (error) => {
      const originalRequest = error.config;

      // Se recebeu 401 e não é uma tentativa de refresh
      if (error.response?.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;

        const refreshToken = localStorage.getItem('refresh_token');
        
        if (refreshToken) {
          try {
            // Tentar fazer refresh do token
            const response = await authApi.post('/auth/refresh', {}, {
              headers: {
                'Authorization': `Bearer ${refreshToken}`
              }
            });

            const { access_token } = response.data;
            
            // Atualizar token no localStorage
            localStorage.setItem('access_token', access_token);
            
            // Atualizar header da requisição original
            originalRequest.headers.Authorization = `Bearer ${access_token}`;
            
            // Reexecutar a requisição original
            return axios(originalRequest);
          } catch (refreshError) {
            // Se o refresh falhou, fazer logout
            console.log('Token refresh falhou, fazendo logout...');
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user');
            
            // Chamar callback para redirecionar para login
            onTokenExpired();
            return Promise.reject(refreshError);
          }
        } else {
          // Não há refresh token, fazer logout
          console.log('Sem refresh token, fazendo logout...');
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          localStorage.removeItem('user');
          
          onTokenExpired();
          return Promise.reject(error);
        }
      }

      return Promise.reject(error);
    }
  );
}
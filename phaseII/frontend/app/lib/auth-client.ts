// Simple auth client for custom JWT implementation
export const authClient = {
  getSession: async () => {
    const token = localStorage.getItem('access_token');
    if (!token) return null;

    // Decode JWT to get expiration time
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const exp = payload.exp * 1000;
      if (Date.now() >= exp) {
        localStorage.removeItem('access_token');
        return null;
      }

      return {
        token,
        user: {
          id: payload.sub,
          email: payload.email || '',
          createdAt: payload.iat ? new Date(payload.iat * 1000).toISOString() : new Date().toISOString()
        }
      };
    } catch (error) {
      console.error('Error decoding token:', error);
      localStorage.removeItem('access_token');
      return null;
    }
  },

  signIn: {
    email: async ({ email, password, callbackURL }: { email: string, password: string, callbackURL?: string }) => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:8000"}/api/auth/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: new URLSearchParams({
            email,
            password
          })
        });

        const data = await response.json();

        if (response.ok) {
          localStorage.setItem('access_token', data.access_token);
          if (callbackURL) {
            window.location.href = callbackURL;
          }
          return { data, error: null };
        } else {
          return { data: null, error: data };
        }
      } catch (error) {
        return { data: null, error: { message: 'Network error' } };
      }
    }
  },

  signUp: {
    email: async ({ email, password, callbackURL }: { email: string, password: string, callbackURL?: string }) => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:8000"}/api/auth/register`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email,
            password
          })
        });

        const data = await response.json();

        if (response.ok) {
          // Automatically log in after registration
          const loginResponse = await fetch(`${process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:8000"}/api/auth/login`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
              email,
              password
            })
          });

          const loginData = await loginResponse.json();

          if (loginResponse.ok) {
            localStorage.setItem('access_token', loginData.access_token);
            if (callbackURL) {
              window.location.href = callbackURL;
            }
            return { data: loginData, error: null };
          } else {
            return { data: null, error: loginData };
          }
        } else {
          return { data: null, error: data };
        }
      } catch (error) {
        return { data: null, error: { message: 'Network error' } };
      }
    }
  },

  signOut: async () => {
    localStorage.removeItem('access_token');
    window.location.href = '/';
  }
};
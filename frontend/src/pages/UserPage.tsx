import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { UserCard } from '../components/UserCard';
import { fetchUser } from '../services/api';
import type { User } from '../types/user';

export const UserPage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadUser = async () => {
      if (!id || isNaN(Number(id))) {
        setError('Invalid user ID');
        return;
      }

      setLoading(true);
      setError(null);
      
      try {
        const response = await fetchUser(Number(id));
        setUser(response.data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load user');
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    loadUser();
  }, [id]);

  const handleUserIdChange = (newId: string) => {
    if (newId && !isNaN(Number(newId)) && Number(newId) > 0) {
      navigate(`/user/${newId}`);
    }
  };

  return (
    <div className="user-page">
      <div className="header">
        <h1>User Profile</h1>
        <div className="user-id-input">
          <label htmlFor="userId">User ID: </label>
          <input
            id="userId"
            type="number"
            min="1"
            value={id || ''}
            onChange={(e) => handleUserIdChange(e.target.value)}
            placeholder="Enter user ID"
          />
        </div>
      </div>

      {loading && (
        <div className="loading">
          <p>Loading user data...</p>
        </div>
      )}

      {error && (
        <div className="error">
          <p>Error: {error}</p>
        </div>
      )}

      {user && !loading && !error && (
        <UserCard user={user} />
      )}

      {!id && !loading && (
        <div className="instructions">
          <p>Enter a user ID above to view user details, or visit /user/1 to /user/12 for sample users.</p>
        </div>
      )}
    </div>
  );
};
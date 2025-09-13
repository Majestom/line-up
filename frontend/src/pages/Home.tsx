import { useNavigate } from 'react-router-dom';

export const Home = () => {
  const navigate = useNavigate();

  const sampleUsers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];

  return (
    <div className="home-page">
      <div className="header">
        <h1>User Data Application</h1>
        <p>This application demonstrates fetching and displaying user data from an API.</p>
      </div>

      <div className="content">
        <section className="instructions">
          <h2>How to use</h2>
          <ul>
            <li>Click on a sample user ID below</li>
            <li>Or navigate directly to /user/[id] in the URL</li>
            <li>Use the input field on the user page to switch between users</li>
          </ul>
        </section>

        <section className="sample-users">
          <h2>Sample Users</h2>
          <div className="user-grid">
            {sampleUsers.map((userId) => (
              <button
                key={userId}
                className="user-button"
                onClick={() => navigate(`/user/${userId}`)}
              >
                User {userId}
              </button>
            ))}
          </div>
        </section>

        <section className="api-info">
          <h2>API Information</h2>
          <p>
            This application fetches data from a Python FastAPI backend that proxies 
            requests to the <a href="https://reqres.in" target="_blank" rel="noopener noreferrer">
            reqres.in API</a>.
          </p>
          <ul>
            <li>Backend: Python FastAPI (running on port 8000)</li>
            <li>Frontend: React with TypeScript and Vite (running on port 5173)</li>
            <li>Data Source: reqres.in API</li>
          </ul>
        </section>
      </div>
    </div>
  );
};
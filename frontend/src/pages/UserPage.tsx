import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import styled from 'styled-components';
import { UserCard } from '../components/UserCard';
import { fetchUser, ApiError } from '../services/api';
import { Container } from '../styles/GlobalStyles';

const PageContainer = styled(Container)`
  max-width: 800px;
`;

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;

  @media (max-width: 768px) {
    flex-direction: column;
    text-align: center;
  }
`;

const Title = styled.h1`
  margin: 0;
  color: #333;
`;

const UserIdInput = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const Label = styled.label`
  font-weight: bold;
  color: #333;
`;

const Input = styled.input`
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  width: 120px;
`;

const Instructions = styled.div`
  text-align: center;
  padding: 2rem;
  color: #666;
  background: #f8f9fa;
  border-radius: 8px;
  margin: 1rem 0;
`;

export const UserPage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const {
    data: userResponse,
    isLoading,
    error,
  } = useQuery({
    queryKey: ['user', id],
    queryFn: () => fetchUser(Number(id)),
    enabled: Boolean(id && !isNaN(Number(id)) && Number(id) > 0),
    retry: (failureCount, error) => {
      // Don't retry on 404 errors
      if (error instanceof ApiError && error.statusCode === 404) {
        return false;
      }
      return failureCount < 2;
    },
  });

  const handleUserIdChange = (newId: string) => {
    if (newId && !isNaN(Number(newId)) && Number(newId) > 0) {
      navigate(`/user/${newId}`);
    }
  };

  const getErrorMessage = () => {
    if (error instanceof ApiError) {
      return error.message;
    }
    if (error instanceof Error) {
      return error.message;
    }
    return 'Failed to load user';
  };

  const shouldShowCard = Boolean(id && !isNaN(Number(id)) && Number(id) > 0);
  const shouldShowInstructions = !id && !isLoading;

  return (
    <PageContainer>
      <Header>
        <Title>User Profile</Title>
        <UserIdInput>
          <Label htmlFor="userId">User ID:</Label>
          <Input
            id="userId"
            type="number"
            min="1"
            value={id || ''}
            onChange={(e) => handleUserIdChange(e.target.value)}
            placeholder="Enter user ID"
          />
        </UserIdInput>
      </Header>

      {shouldShowCard && (
        <UserCard
          user={userResponse?.data}
          loading={isLoading}
          error={error ? getErrorMessage() : undefined}
        />
      )}

      {shouldShowInstructions && (
        <Instructions>
          <p>Enter a user ID above to view user details, or visit /user/1 to /user/12 for sample users.</p>
        </Instructions>
      )}
    </PageContainer>
  );
};
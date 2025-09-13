import styled from 'styled-components';
import type { User } from '../types/user';

type UserCardProps = {
  user?: User;
  loading?: boolean;
  error?: string;
};

const CardContainer = styled.div`
  background: white;
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 2rem;
  align-items: center;
  max-width: 600px;
  margin: 0 auto;

  @media (max-width: 768px) {
    flex-direction: column;
    text-align: center;
  }
`;

const Avatar = styled.img`
  width: 128px;
  height: 128px;
  border-radius: 50%;
  object-fit: cover;
`;

const UserInfo = styled.div`
  flex: 1;
`;

const UserName = styled.h2`
  margin: 0 0 1rem 0;
  color: #333;
  font-size: 1.8rem;
`;

const UserId = styled.p`
  color: #666;
  font-size: 1rem;
  margin: 0.5rem 0;
`;

const UserEmail = styled.p`
  color: #007bff;
  font-size: 1.1rem;
  margin: 0.5rem 0;
  word-break: break-word;
`;


const LoadingSkeleton = styled.div`
  display: flex;
  gap: 2rem;
  align-items: center;
  max-width: 600px;
  margin: 0 auto;

  @media (max-width: 768px) {
    flex-direction: column;
    text-align: center;
  }
`;

const SkeletonAvatar = styled.div`
  width: 128px;
  height: 128px;
  border-radius: 50%;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;

  @keyframes loading {
    0% {
      background-position: 200% 0;
    }
    100% {
      background-position: -200% 0;
    }
  }
`;

const SkeletonText = styled.div<{ width?: string; height?: string }>`
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
  border-radius: 4px;
  width: ${props => props.width || '100%'};
  height: ${props => props.height || '1rem'};
  margin: 0.25rem 0;

  @keyframes loading {
    0% {
      background-position: 200% 0;
    }
    100% {
      background-position: -200% 0;
    }
  }
`;

const SkeletonInfo = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const ErrorContainer = styled.div`
  text-align: center;
  padding: 2rem;
  color: #dc3545;
  background: #f8d7da;
  border-radius: 8px;
  margin: 1rem 0;
  max-width: 600px;
  margin: 0 auto;
`;


export const UserCard = ({ user, loading, error }: UserCardProps) => {
  if (loading) {
    return (
      <CardContainer>
        <LoadingSkeleton>
          <SkeletonAvatar />
          <SkeletonInfo>
            <SkeletonText height="2rem" width="60%" />
            <SkeletonText height="1rem" width="30%" />
            <SkeletonText height="1rem" width="80%" />
          </SkeletonInfo>
        </LoadingSkeleton>
      </CardContainer>
    );
  }

  if (error) {
    return (
      <ErrorContainer>
        <p>Error: {error}</p>
      </ErrorContainer>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <CardContainer>
      <Avatar
        src={user.avatar}
        alt={`${user.first_name} ${user.last_name}`}
        loading="lazy"
      />
      <UserInfo>
        <UserName>{user.first_name} {user.last_name}</UserName>
        <UserId>ID: {user.id}</UserId>
        <UserEmail>{user.email}</UserEmail>
      </UserInfo>
    </CardContainer>
  );
};
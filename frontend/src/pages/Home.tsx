import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { Container } from '../styles/GlobalStyles';

const HomePage = styled(Container)`
  text-align: center;
`;

const HeaderSection = styled.div`
  margin-bottom: 2rem;
`;

const Title = styled.h1`
  color: #333;
  margin-bottom: 0.5rem;
`;

const Subtitle = styled.p`
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 2rem;
`;

const Content = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const Section = styled.section`
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: left;

  &.api-info {
    background: #e9f7ff;
  }
`;

const SectionTitle = styled.h2`
  margin-top: 0;
  color: #333;
`;

const InstructionList = styled.ul`
  margin: 1rem 0;
  padding-left: 1.5rem;
`;

const UserGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 1rem;
  margin: 1rem 0;
`;

const UserButton = styled.button`
  padding: 1rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;

  &:hover {
    background: #0056b3;
  }

  @media (max-width: 768px) {
    min-width: 100px;
  }
`;

const ApiList = styled.ul`
  margin: 1rem 0;
  padding-left: 1.5rem;
`;

const ExternalLink = styled.a`
  color: #007bff;

  &:hover {
    text-decoration: underline;
  }
`;

export const Home = () => {
  const navigate = useNavigate();

  const sampleUsers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];

  return (
    <HomePage>
      <HeaderSection>
        <Title>User Data Application</Title>
        <Subtitle>This application demonstrates fetching and displaying user data from an API.</Subtitle>
      </HeaderSection>

      <Content>
        <Section>
          <SectionTitle>How to use</SectionTitle>
          <InstructionList>
            <li>Click on a sample user ID below</li>
            <li>Or navigate directly to /user/[id] in the URL</li>
            <li>Use the input field on the user page to switch between users</li>
          </InstructionList>
        </Section>

        <Section>
          <SectionTitle>Sample Users</SectionTitle>
          <UserGrid>
            {sampleUsers.map((userId) => (
              <UserButton
                key={userId}
                onClick={() => navigate(`/user/${userId}`)}
              >
                User {userId}
              </UserButton>
            ))}
          </UserGrid>
        </Section>

        <Section className="api-info">
          <SectionTitle>API Information</SectionTitle>
          <p>
            This application fetches data from a Python FastAPI backend that proxies
            requests to the <ExternalLink href="https://reqres.in" target="_blank" rel="noopener noreferrer">
            reqres.in API</ExternalLink>.
          </p>
          <ApiList>
            <li>Backend: Python FastAPI (running on port 8000)</li>
            <li>Frontend: React with TypeScript and Vite (running on port 5173)</li>
            <li>Data Source: reqres.in API</li>
          </ApiList>
        </Section>
      </Content>
    </HomePage>
  );
};
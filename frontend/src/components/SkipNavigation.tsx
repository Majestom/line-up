import styled from 'styled-components';

const SkipLink = styled.a`
  position: absolute;
  top: -40px;
  left: 6px;
  background: #000;
  color: #fff;
  padding: 8px;
  text-decoration: none;
  border-radius: 4px;
  z-index: 1000;

  &:focus {
    top: 6px;
  }
`;

export const SkipNavigation = () => {
  return (
    <SkipLink href="#main-content">
      Skip to main content
    </SkipLink>
  );
};
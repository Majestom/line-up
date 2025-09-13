import type { User } from '../types/user';

interface UserCardProps {
  user: User;
}

export const UserCard = ({ user }: UserCardProps) => {
  return (
    <div className="user-card">
      <div className="user-avatar">
        <img src={user.avatar} alt={`${user.first_name} ${user.last_name}`} />
      </div>
      <div className="user-info">
        <h2>{user.first_name} {user.last_name}</h2>
        <p className="user-id">ID: {user.id}</p>
        <p className="user-email">{user.email}</p>
      </div>
    </div>
  );
};
import React,{ useState } from "react";
import Layout from "./components/Layout";
import Dashboard from "./views/Dashboard";
import RankingApp from "./views/RankingApp";
import AuthPage from "./views/AuthPage";
import Profile from "./views/Profile";
import { AppType, UserProfile } from "./types";

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [activeTab, setActiveTab] = useState<AppType>(AppType.DASHBOARD);

  const [user, setUser] = useState<UserProfile>({
    name: "Jane Doe",
    designation: "Principal Analyst",
    authLevel: "Admin",
    avatar: undefined,
  });


  if (!isAuthenticated) {
    return (
      <Layout variant="auth">
        <AuthPage
          onLoginSuccess={() => {
            setIsAuthenticated(true);
            setActiveTab(AppType.DASHBOARD);
          }}
        />
      </Layout>
    );
  }

  const renderContent = () => {
    switch (activeTab) {
      case AppType.DASHBOARD:
        return <Dashboard />;
      case AppType.RANKING:
        return <RankingApp />;
      case AppType.PROFILE:
        return (
          <Profile
            user={user}
            onUserUpdate={setUser}
            onLogout={() => setIsAuthenticated(false)}
          />
        ); 
      default:
        return <Dashboard />;
    }
  };

  return (
    <Layout
      variant="app"
      activeTab={activeTab}
      setActiveTab={setActiveTab}
      user={user}
      onLogout={() => setIsAuthenticated(false)}
    >
      {renderContent()}
    </Layout>
  );
}

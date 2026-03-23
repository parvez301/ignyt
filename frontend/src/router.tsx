import { Navigate, Route, Routes } from "react-router-dom";
import { useAuthStore } from "@/stores/authStore";
import ChapterMapPage from "@/pages/ChapterMapPage";
import DailyChallengePage from "@/pages/DailyChallengePage";
import HomePage from "@/pages/HomePage";
import LeaderboardPage from "@/pages/LeaderboardPage";
import LearnPage from "@/pages/LearnPage";
import LoginPage from "@/pages/LoginPage";
import MasterPage from "@/pages/MasterPage";
import PracticePage from "@/pages/PracticePage";
import ProfilePage from "@/pages/ProfilePage";
import ResultsPage from "@/pages/ResultsPage";
import ReviewPage from "@/pages/ReviewPage";
import SignupPage from "@/pages/SignupPage";

function Protected({ children }: { children: React.ReactNode }) {
  const token = useAuthStore((s) => s.token);
  if (!token) return <Navigate to="/login" replace />;
  return <>{children}</>;
}

export function AppRouter() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup" element={<SignupPage />} />
      <Route
        path="/"
        element={
          <Protected>
            <HomePage />
          </Protected>
        }
      />
      <Route
        path="/chapter/:chapterId"
        element={
          <Protected>
            <ChapterMapPage />
          </Protected>
        }
      />
      <Route
        path="/learn/:topicId"
        element={
          <Protected>
            <LearnPage />
          </Protected>
        }
      />
      <Route
        path="/practice/:topicId"
        element={
          <Protected>
            <PracticePage />
          </Protected>
        }
      />
      <Route
        path="/master/:topicId"
        element={
          <Protected>
            <MasterPage />
          </Protected>
        }
      />
      <Route
        path="/results/:topicId"
        element={
          <Protected>
            <ResultsPage />
          </Protected>
        }
      />
      <Route
        path="/leaderboard"
        element={
          <Protected>
            <LeaderboardPage />
          </Protected>
        }
      />
      <Route
        path="/profile"
        element={
          <Protected>
            <ProfilePage />
          </Protected>
        }
      />
      <Route
        path="/daily-challenge"
        element={
          <Protected>
            <DailyChallengePage />
          </Protected>
        }
      />
      <Route
        path="/review"
        element={
          <Protected>
            <ReviewPage />
          </Protected>
        }
      />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

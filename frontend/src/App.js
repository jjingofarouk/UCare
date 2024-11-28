import "bootstrap/dist/css/bootstrap.min.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useSelector } from "react-redux";
import ICD from "./components/icd/ICD";
import Header from "./components/header/Header";
import Dashboard from "./components/dashboard/Dashboard";
import PatientMainPage from "./components/patients/PatientMainPage";
import TodaySchedule from "./components/appointmens/TodaySchedule";
import ProtectedRoute from "./components/routers/ProtectedRoute";
import { ToastContainer } from "react-toastify";
import Container from "react-bootstrap/esm/Container";

const App = () => {
  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);

  return (
    <Container bg="dark" fluid className="p-0 m-0" data-bs-theme="dark">
      <ToastContainer />
      <BrowserRouter>
        <Header />
        <Routes>
          <Route index element={<div>Access limited</div>} />
          <Route
            path="dashboard"
            element={
              <ProtectedRoute isAuthenticated={isAuthenticated}>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="patients"
            element={
              <ProtectedRoute isAuthenticated={isAuthenticated}>
                <PatientMainPage expand="lg" />
              </ProtectedRoute>
            }
          />
          <Route
            path="icd"
            element={
              <ProtectedRoute isAuthenticated={isAuthenticated}>
                <ICD expand="lg" />
              </ProtectedRoute>
            }
          />
          <Route
            path="today-schedule"
            element={
              <ProtectedRoute isAuthenticated={isAuthenticated}>
                <TodaySchedule />
              </ProtectedRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </Container>
  );
};

export default App;

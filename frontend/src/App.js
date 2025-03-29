import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ClientPage from "./ClientPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/:slug" element={<ClientPage />} />
      </Routes>
    </Router>
  );
}

export default App;

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ClientPage from "./ClientPage";
import Success from "./Success";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/success" element={<Success />} />
        <Route path="/:slug" element={<ClientPage />} />
      </Routes>
    </Router>
  );
}

export default App;

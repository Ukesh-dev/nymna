import {
  Route,
  RouterProvider,
  createBrowserRouter,
  createRoutesFromElements,
} from "react-router-dom";
import IndexPage from "../layout/IndexPage";
import Incidents from "../views/Incidents/Incidents";
import IncidentDetails from "../views/Incidents/components/IncidentDetails";
import Home from "../views";
import Analyze from "../views/Analyze";

function Routes() {
  const router = createBrowserRouter(
    createRoutesFromElements(
      <>
        <Route path="/" element={<IndexPage />}>
          <Route index element={<Home />} />
          <Route path="analyze" element={<Analyze />} />
          <Route path="incidents" element={<Incidents />} />
          <Route path="incidents/:incident" element={<IncidentDetails />} />
        </Route>
      </>,
    ),
  );
  return (
    <>
      <RouterProvider router={router} />
    </>
  );
}

export default Routes;

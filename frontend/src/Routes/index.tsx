import {
  Route,
  RouterProvider,
  createBrowserRouter,
  createRoutesFromElements,
} from "react-router-dom";
import IndexPage from "../layout/IndexPage";
import Incidents from "../views/Incidents/Incidents";
import IncidentDetails from "../views/Incidents/components/IncidentDetails";

function Routes() {
  const router = createBrowserRouter(
    createRoutesFromElements(
      <>
        <Route path="/" element={<IndexPage />}>
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

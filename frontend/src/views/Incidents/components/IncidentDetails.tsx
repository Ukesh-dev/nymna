import { useQuery } from "@tanstack/react-query";
import ReactPlayer from "react-player";
import { useParams } from "react-router-dom";
import { getSingleIncidents } from "../../../api/incidentsApi";
import { IncidentType } from "./IncidentTable";
import { cn } from "../../../lib/utils";
import { useEffect } from "react";

const IncidentDetails = () => {
  const params = useParams() as { incident: string };
  useEffect(() => {
    document.title = "Incidents";
  }, []);
  const { data } = useQuery({
    queryKey: [params.incident],
    queryFn: () =>
      getSingleIncidents<{
        data: IncidentType["data"][number];
        success: boolean;
      }>(params.incident),
  });
  return (
    <div className="lg:pl-72">
      <div className="p-12">
        <div className=" sm:px-0">
          <h3 className="text-base font-semibold leading-7 text-white">
            Incident Information
          </h3>
          <p className="mt-1 max-w-2xl text-sm leading-6 text-gray-400">
            Details of Incidents
          </p>
        </div>
        {data && data.data && (
          <>
            <div className="mt-6 border-t border-white/10">
              <dl className="divide-y divide-white/10">
                <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
                  <dt className="text-sm font-medium leading-6 text-white">
                    Source
                  </dt>
                  <dd className="mt-1 text-sm leading-6 text-gray-400 sm:col-span-2 sm:mt-0">
                    {data.data.data.source}
                  </dd>
                </div>
                <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
                  <dt className="text-sm font-medium leading-6 text-white">
                    Incident Confidence
                  </dt>
                  <dd className="mt-1 text-sm leading-6 text-gray-400 flex gap-6 items-center sm:col-span-2 sm:mt-0">
                    <div className="relative min-w-[80px] max-w-[150px]  bg-gray-600 h-1">
                      <div
                        className={cn(
                          "absolute  left-0 top-0 h-1",
                          data.data.data.confidence * 100 < 20
                            ? "bg-red-500"
                            : data.data.data.confidence * 100 >= 20 &&
                                data.data.data.confidence * 100 <= 40
                              ? "bg-amber-500"
                              : "bg-green-500",
                        )}
                        style={{
                          width: `${data.data.data.confidence * 100}%`,
                        }}
                      ></div>
                    </div>
                    ({data.data.data.confidence * 100}%)
                  </dd>
                </div>
                <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
                  <dt className="text-sm font-medium leading-6 text-white">
                    Status
                  </dt>
                  <dd className="mt-1 capitalize text-sm leading-6 text-gray-400 sm:col-span-2 sm:mt-0">
                    {data.data.data.status}
                  </dd>
                </div>
                <div className="px-4 py-6">
                  {data.data.data.video && (
                    <iframe
                      src={data.data.data.video}
                      style={{
                        width:"100%",
                        minHeight:"600px"
                      }}
                    />
                  )}
                </div>
              </dl>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default IncidentDetails;

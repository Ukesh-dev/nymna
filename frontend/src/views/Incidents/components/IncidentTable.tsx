import {
  ColumnDef,
  PaginationState,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import { Button } from "@headlessui/react";
import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { DataTablePagination } from "./TablePagination";
import { getIncidents } from "../../../api/incidentsApi";
import { cn } from "../../../lib/utils";
import { useIncident } from "../../../store/useIncident";

const statuses: Record<string, string> = {
  minor: "text-green-400 bg-green-400/10",
  mediocre: "text-amber-400 bg-amber-400/10",
  severe: "text-rose-400 bg-rose-400/10",
};

export type IncidentType = {
  type: "new_alert" | "";
  current: number;
  total: number;
  data: {
    id: number;
    source: string;
    confidence: number;
    video: string;
    status: "minor" | "mideocre" | "servere";
    timestamp_start: number;
    timestamp_end: number;
  }[];
};

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(" ");
}

export default function IncidentTable() {
  const navigate = useNavigate();
  const columns: ColumnDef<IncidentType["data"][number]>[] = [
    {
      header: "S.N",
      cell: (originalRow) => <span>{originalRow.row.index + 1}.</span>,
    },
    {
      cell: (originalRow) => {
        return (
          <div className="flex items-center gap-2">
            <span></span>
            <div>
              <span>{originalRow.row.original.source}</span>
            </div>
          </div>
        );
      },
      accessorKey: "source",
      header: "Source",
    },

    {
      accessorKey: "status",
      header: "Status",
      cell: (original) => (
        <div className="flex items-center justify-end gap-x-2 sm:justify-start">
          <div
            className={classNames(
              statuses[original.row.original.status],
              "flex-none rounded-full p-1",
            )}
          >
            <div className="h-1.5 w-1.5 rounded-full bg-current" />
          </div>
          <div className="hidden capitalize text-white sm:block">
            {original.row.original.status}
          </div>
        </div>
      ),
    },
    {
      accessorKey: "confidence",
      header: "Incident Confidence",
      cell: (original) => {
        return (
          <div className="flex gap-4 items-center">
            <div className="relative  min-w-[150px] max-w-[150px] bg-gray-600 h-1">
              <div
                className={cn(
                  "absolute  left-0 top-0 h-1",
                  original.row.original.confidence * 100 < 20
                    ? "bg-red-500"
                    : original.row.original.confidence * 100 >= 20 &&
                        original.row.original.confidence * 100 <= 40
                      ? "bg-amber-500"
                      : "bg-green-500",
                )}
                style={{ width: `${original.row.original.confidence * 100}%` }}
              ></div>
            </div>
            <span className="text-sm">
              ({original.row.original.confidence * 100}%)
            </span>{" "}
          </div>
        );
      },
    },
    {
      id: "actions",
      cell: (original) => {
        return (
          <Button
            onClick={() => {
              navigate(`${original.row.original.id}`);
            }}
            className="inline-flex items-center gap-2 rounded-md bg-gray-700 py-1.5 px-3 text-sm/6 font-semibold text-white shadow-inner shadow-white/10 focus:outline-none data-[hover]:bg-gray-600 data-[open]:bg-gray-700 data-[focus]:outline-1 data-[focus]:outline-white"
          >
            View
          </Button>
        );
      },
    },
  ];

  const { data, currentData, setData, setCurrentData } = useIncident();

  const [{ pageIndex, pageSize }, setPagination] = useState<PaginationState>({
    pageIndex: 0,
    pageSize: 10,
  });

  const fetchDataOptions = useMemo(
    () => ({
      pageIndex,
      pageSize,
    }),
    [pageIndex, pageSize],
  );
  const pagination = useMemo(
    () => ({
      pageIndex,
      pageSize,
    }),
    [pageIndex, pageSize],
  );

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getIncidents<IncidentType>(fetchDataOptions);
        // data.data.data
        setData(data.data);
        setCurrentData([...data.data.data, ...currentData]);
      } catch (err) {
        console.log(err);
      }
    };
    if (currentData.length === 0) {
      fetchData();
    }
  }, [currentData, fetchDataOptions, setCurrentData, setData]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getIncidents<IncidentType>(fetchDataOptions);
        setCurrentData([...data.data.data]);
      } catch (err) {
        console.log(err);
      }
    };
    if (currentData.length > 0) {
      fetchData();
    }
  }, [currentData.length, fetchDataOptions, setCurrentData]);

  const table = useReactTable({
    data: currentData ?? [],
    columns: columns,
    pageCount: data?.total ?? 0,
    autoResetPageIndex: false,
    autoResetExpanded: true,

    state: {
      pagination: pagination,
    },
    onPaginationChange: setPagination,
    getCoreRowModel: getCoreRowModel(),
    manualPagination: true,
    debugTable: true,
  });
  return (
    <div className="bg-gray-transparent py-10 lg:pl-72">
      <h2 className="px-4 text-base font-semibold leading-7 text-white sm:px-6 lg:px-8">
        Latest incident
      </h2>
      <table className="mt-6 w-full whitespace-nowrap text-left">
        <thead className="border-b border-white/10 text-sm leading-6 text-white">
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => {
                return (
                  <th
                    key={header.id}
                    scope="col"
                    className="py-2 pl-4 pr-8 font-semibold sm:pl-6 lg:pl-8"
                  >
                    {header.isPlaceholder
                      ? null
                      : flexRender(
                          header.column.columnDef.header,
                          header.getContext(),
                        )}
                  </th>
                );
              })}
            </tr>
          ))}
        </thead>
        <tbody className="divide-y divide-white/5">
          {table.getRowModel().rows?.length > 0 ? (
            table.getRowModel().rows.map((row) => (
              <tr key={row.id}>
                {row.getVisibleCells().map((cell) => (
                  <td
                    className="py-4 pl-4 pr-8 sm:pl-6 lg:pl-8 text-white"
                    key={cell.id}
                  >
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            ))
          ) : (
            <tr className="text-white py-4 pl-4 pr-8 sm:pl-6 lg:pl-8">
              <td colSpan={columns.length} className="h-24 text-center">
                No results
              </td>
            </tr>
          )}
        </tbody>
      </table>

      <DataTablePagination table={table} />
    </div>
  );
}

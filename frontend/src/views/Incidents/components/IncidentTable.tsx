import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import { Button } from "@headlessui/react";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Dialogs from "../../../components/ui/Dialogs";
import { useQuery } from "@tanstack/react-query";
import api from "../../../api";

const statuses: Record<string, string> = {
  Minor: "text-green-400 bg-green-400/10",
  Mediocre: "text-amber-400 bg-amber-400/10",
  Severe: "text-rose-400 bg-rose-400/10",
};

export type IncidentType = {
  type: "new_alert" | "";
  data: {
    id: number;
    source: string;
    confidence: number;
    status: "minor" | "mideocre" | "servere";
    timestamp_start: number;
    timestamp_end: number;
  };
};
const activityItems: IncidentType[] = [];

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(" ");
}

export default function IncidentTable() {
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();
  const columns: ColumnDef<IncidentType>[] = [
    {
      header: "S.N",
      cell: (originalRow) => <span>{originalRow.row.index + 1}.</span>,
      // footer: () => <span>Total</span>,
    },
    {
      // accessorFn: (originalRow) => {
      //   return originalRow.employee;
      // },
      cell: (originalRow) => {
        return (
          <div className="flex items-center gap-2">
            <span>
              {/* <Avatar> */}
              {/*   <AvatarFallback></AvatarFallback> */}
              {/* </Avatar> */}
            </span>
            <div>
              <span>{originalRow.row.original.data.source}</span>
              {/* <span className="block font-light text-xs">APEM</span> */}
            </div>
            {/* <CalendarModal calendarInfo={originalRow.row.original.employee} /> */}
          </div>
        );
      },
      accessorKey: "source",
      header: "Source",
    },

    {
      accessorKey: "status",
      cell: (original) => (
        <div className="flex items-center justify-end gap-x-2 sm:justify-start">
          {/* <time
            className="text-gray-400 sm:hidden"
            dateTime={original.row.original.dateTime}
          >
            {original.row.original.data.status}
          </time> */}
          <div
            className={classNames(
              statuses[original.row.original.data.status],
              "flex-none rounded-full p-1",
            )}
          >
            <div className="h-1.5 w-1.5 rounded-full bg-current" />
          </div>
          <div className="hidden text-white sm:block">
            {original.row.original.data.status}
          </div>
        </div>
      ),
    },
    {
      accessorKey: "confidence",
      header: "Confidence",
      cell: (original) => <span>{original.row.original.data.confidence}</span>,
    },
    {
      id: "actions",
      // cell: ({ row }) => <DataTableRowActions row={row} />,
      cell: (original) => {
        return (
          <Button
            onClick={() => {
              navigate(`${original.row.original.data.source}`);
            }}
            className="inline-flex items-center gap-2 rounded-md bg-gray-700 py-1.5 px-3 text-sm/6 font-semibold text-white shadow-inner shadow-white/10 focus:outline-none data-[hover]:bg-gray-600 data-[open]:bg-gray-700 data-[focus]:outline-1 data-[focus]:outline-white"
          >
            View
          </Button>
        );
      },
    },
  ];
  const [data, setData] = useState(() => activityItems);
  /* const { data } = useQuery({
    queryKey: ["incidents"],
    queryFn: () => api.get<IncidentType[]>("/api"),
  }); */

  useEffect(() => {
    const websocket = new WebSocket("ws://127.0.0.1:8000/report/alert/");
    websocket.onopen = () => {
      console.log("connection established");
    };
    websocket.onclose = () => {
      console.log("connection closed");
    };
    websocket.onmessage = (event) => {
      const events = JSON.parse(event.data) as IncidentType;
      // const queryKey = [events.data.id, ]
      setData((prev) => [events, ...prev]);
      setOpen(true);
    };
    () => {
      websocket.close();
    };
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await api.get<IncidentType[]>("/reports/");
        console.log(data);
        setData(data.data);
      } catch (err) {
        console.log(err);
      }
    };
    if (data.length === 0) {
      fetchData();
    }
  }, [data]);

  const table = useReactTable({
    data: data,
    columns: columns,
    // pageCount: dataQuery.data?.total_pages ?? 0,
    autoResetPageIndex: false,
    // state: {
    //   pagination: pagination,
    //   columnFilters: columnFilter,
    //   sorting,
    // },
    // onColumnFiltersChange: setColumnFilters,
    // onSortingChange: setSorting,
    // onPaginationChange: setPagination,
    getCoreRowModel: getCoreRowModel(),
    // manualFiltering: true,
    // manualPagination: true,
    // manualSorting: true,
    // enableMultiSort: true,
  });
  return (
    <div className="bg-gray-transparent py-10 lg:pl-72">
      <h2 className="px-4 text-base font-semibold leading-7 text-white sm:px-6 lg:px-8">
        Latest incident
      </h2>
      <table className="mt-6 w-full whitespace-nowrap text-left">
        {/* <colgroup> */}
        {/*   <col className="w-full sm:w-4/12" /> */}
        {/*   <col className="lg:w-4/12" /> */}
        {/*   <col className="lg:w-2/12" /> */}
        {/*   <col className="lg:w-1/12" /> */}
        {/*   <col className="lg:w-1/12" /> */}
        {/* </colgroup> */}
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
      <Dialogs
        message="hell"
        open={open}
        setOpen={(open: boolean) => {
          setOpen(open);
        }}
      />
    </div>
  );
}

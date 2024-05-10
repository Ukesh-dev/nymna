import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import {
  Menu,
  MenuButton,
  MenuItem,
  MenuItems,
  Transition,
} from "@headlessui/react";
import { EllipsisVertical, PencilIcon } from "lucide-react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

const statuses = {
  Minor: "text-green-400 bg-green-400/10",
  Mediocre: "text-amber-400 bg-amber-400/10",
  Severe: "text-rose-400 bg-rose-400/10",
};

export type IncidentType = {
  user: {
    name: string;
  };
  commit: string;
  status: string;
  branch: string;
  duration: string;
  date: string;
  dateTime: string;
};
const activityItems = [
  {
    user: {
      name: "Michael Foster",
    },
    commit: "2d89f0c8",
    branch: "main",
    status: "Minor",
    duration: "25s",
    date: "45 minutes ago",
    dateTime: "2023-01-23T11:00",
  },
  {
    user: {
      name: "Lindsay Walton",
    },
    commit: "249df660",
    branch: "main",
    status: "Severe",
    duration: "1m 32s",
    date: "3 hours ago",
    dateTime: "2023-01-23T09:00",
  },
  {
    user: {
      name: "Courtney Henry",
    },
    commit: "11464223",
    branch: "main",
    status: "Mediocre",
    duration: "1m 4s",
    date: "12 hours ago",
    dateTime: "2023-01-23T00:00",
  },
  {
    user: {
      name: "Courtney Henry",
    },
    commit: "dad28e95",
    branch: "main",
    status: "Severe",
    duration: "2m 15s",
    date: "2 days ago",
    dateTime: "2023-01-21T13:00",
  },
  {
    user: {
      name: "Michael Foster",
    },
    commit: "624bc94c",
    branch: "main",
    status: "Severe",
    duration: "1m 12s",
    date: "5 days ago",
    dateTime: "2023-01-18T12:34",
  },
  {
    user: {
      name: "Courtney Henry",
    },
    commit: "e111f80e",
    branch: "main",
    status: "Minor",
    duration: "1m 56s",
    date: "1 week ago",
    dateTime: "2023-01-16T15:54",
  },
];

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(" ");
}

export default function IncidentTable() {
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
              <span>{originalRow.row.original.user.name}</span>
              {/* <span className="block font-light text-xs">APEM</span> */}
            </div>
            {/* <CalendarModal calendarInfo={originalRow.row.original.employee} /> */}
          </div>
        );
      },
      accessorKey: "name",
      header: "Name",
      footer: (original) => {
        return original.table.getRowCount();
      },
    },

    {
      accessorKey: "Incidents",
      cell: (original) => (
        <div className="flex items-center justify-end gap-x-2 sm:justify-start">
          <time
            className="text-gray-400 sm:hidden"
            dateTime={original.row.original.dateTime}
          >
            {original.row.original.date}
          </time>
          <div
            className={classNames(
              statuses[original.row.original.status],
              "flex-none rounded-full p-1",
            )}
          >
            <div className="h-1.5 w-1.5 rounded-full bg-current" />
          </div>
          <div className="hidden text-white sm:block">
            {original.row.original.status}
          </div>
        </div>
      ),
    },
    {
      id: "actions",
      // cell: ({ row }) => <DataTableRowActions row={row} />,
      cell: (original) => {
        return (
          <Menu>
            <MenuButton className="inline-flex items-center gap-2 rounded-md bg-gray-800 py-1.5 px-3 text-sm/6 font-semibold text-white shadow-inner shadow-white/10 focus:outline-none data-[hover]:bg-gray-700 data-[open]:bg-gray-700 data-[focus]:outline-1 data-[focus]:outline-white">
              <EllipsisVertical className="size-4 fill-white/60" />
            </MenuButton>
            <Transition
              enter="transition ease-out duration-75"
              enterFrom="opacity-0 scale-95"
              enterTo="opacity-100 scale-100"
              leave="transition ease-in duration-100"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <MenuItems
                anchor="bottom end"
                className="w-52 origin-top-right rounded-xl border border-black/50 bg-black/50 p-1 text-sm/6 text-white [--anchor-gap:var(--spacing-1)] focus:outline-none"
              >
                <MenuItem>
                  <button
                    onClick={() => {
                      navigate(`/incidents/${original.row.original.user}`);
                    }}
                    className="group flex w-full items-center gap-2 rounded-lg py-1.5 px-3 data-[focus]:bg-white/10"
                  >
                    <PencilIcon className="size-4 fill-white/30" />
                    Incident Details
                  </button>
                </MenuItem>
              </MenuItems>
            </Transition>
          </Menu>
        );
      },
    },
  ];

  const [data] = useState(() => activityItems);
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
        Latest activity
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
          {table.getRowModel().rows?.length ? (
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
    </div>
  );
}

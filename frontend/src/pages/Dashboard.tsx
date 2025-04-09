import React from 'react';
import { 
  Users,
  Bus,
  TicketIcon,
  Ban
} from 'lucide-react';

const Dashboard = () => {
  const stats = [
    { name: 'Total Bookings', value: '156', icon: TicketIcon, color: 'bg-blue-500' },
    { name: 'Available Buses', value: '12', icon: Bus, color: 'bg-green-500' },
    { name: 'Active Users', value: '892', icon: Users, color: 'bg-purple-500' },
    { name: 'Cancellations', value: '8', icon: Ban, color: 'bg-red-500' },
  ];

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
      
      <div className="mt-6 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((item) => (
          <div
            key={item.name}
            className="bg-white overflow-hidden shadow rounded-lg"
          >
            <div className="p-5">
              <div className="flex items-center">
                <div className={`flex-shrink-0 p-3 rounded-md ${item.color}`}>
                  <item.icon className="h-6 w-6 text-white" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      {item.name}
                    </dt>
                    <dd className="text-2xl font-semibold text-gray-900">
                      {item.value}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Add more dashboard content here */}
    </div>
  );
};

export default Dashboard;
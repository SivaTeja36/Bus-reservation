import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  Home,
  TicketIcon,
  Users,
  Settings,
  LogOut,
  Bus
} from 'lucide-react';
import { useAuthStore } from '../store/authStore';

const Sidebar = () => {
  const logout = useAuthStore((state) => state.logout);

  const navigation = [
    { name: 'Dashboard', icon: Home, href: '/' },
    { name: 'Bookings', icon: TicketIcon, href: '/bookings' },
    { name: 'Users', icon: Users, href: '/users' },
    { name: 'Buses', icon: Bus, href: '/buses' },
    { name: 'Settings', icon: Settings, href: '/settings' },
  ];

  return (
    <div className="hidden md:flex md:flex-shrink-0">
      <div className="flex flex-col w-64">
        <div className="flex flex-col h-0 flex-1 bg-gray-800">
          <div className="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
            <div className="flex items-center flex-shrink-0 px-4">
              <Bus className="h-8 w-8 text-white" />
              <span className="ml-2 text-white text-lg font-semibold">BusRes</span>
            </div>
            <nav className="mt-5 flex-1 px-2 space-y-1">
              {navigation.map((item) => (
                <NavLink
                  key={item.name}
                  to={item.href}
                  className={({ isActive }) =>
                    `group flex items-center px-2 py-2 text-sm font-medium rounded-md ${
                      isActive
                        ? 'bg-gray-900 text-white'
                        : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                    }`
                  }
                >
                  <item.icon className="mr-3 h-5 w-5" />
                  {item.name}
                </NavLink>
              ))}
            </nav>
          </div>
          <div className="flex-shrink-0 flex border-t border-gray-700 p-4">
            <button
              onClick={logout}
              className="flex-shrink-0 w-full group flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-300 hover:bg-gray-700 hover:text-white"
            >
              <LogOut className="mr-3 h-5 w-5" />
              Logout
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
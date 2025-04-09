import React from 'react';
import { Bell, User } from 'lucide-react';
import { useAuthStore } from '../store/authStore';

const Navbar = () => {
  const user = useAuthStore((state) => state.user);

  return (
    <nav className="bg-white border-b border-gray-200 px-4 py-2.5">
      <div className="flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <span className="text-xl font-semibold">Bus Reservation System</span>
        </div>
        
        <div className="flex items-center space-x-4">
          <button className="p-2 hover:bg-gray-100 rounded-full">
            <Bell className="h-5 w-5 text-gray-500" />
          </button>
          
          <div className="flex items-center space-x-2">
            <div className="bg-gray-100 p-2 rounded-full">
              <User className="h-5 w-5 text-gray-500" />
            </div>
            <span className="text-sm font-medium">{user?.name}</span>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
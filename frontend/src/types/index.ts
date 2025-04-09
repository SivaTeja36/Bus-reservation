export interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'branch_manager' | 'operator';
  branchId: string;
}

export interface Branch {
  id: string;
  name: string;
  location: string;
  contactNumber: string;
}

export interface Bus {
  id: string;
  number: string;
  totalSeats: number;
  availableSeats: number;
  route: string;
  departureTime: string;
  arrivalTime: string;
  price: number;
}

export interface Booking {
  id: string;
  busId: string;
  userId: string;
  passengerName: string;
  seatNumber: number;
  status: 'confirmed' | 'cancelled';
  bookingDate: string;
}

import React from 'react';
import { XCircleIcon } from '../icons';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl';
}

// Renamed ModalSimplified to Modal and made it the primary component.
const Modal: React.FC<ModalProps> = ({ isOpen, onClose, title, children, size = 'md' }) => {
  if (!isOpen) return null;

  const sizeClasses = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
  };

  // Using Tailwind CSS classes for transition and animation if desired,
  // for example, by adding 'transition-opacity duration-300 ease-in-out opacity-0 animate-fadeIn'
  // to the outer div and defining 'animate-fadeIn' in tailwind.config.js or a global CSS.
  // For simplicity, keeping it without explicit animation classes here beyond what Tailwind offers by default.
  return (
    <div 
      className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <div className={`bg-white rounded-lg shadow-xl w-full ${sizeClasses[size]} p-6`}>
        <div className="flex justify-between items-center mb-4">
          <h2 id="modal-title" className="text-xl font-semibold text-darkgray">{title}</h2>
          <button 
            onClick={onClose} 
            className="text-mediumgray hover:text-darkgray"
            aria-label="Lukk modal"
          >
            <XCircleIcon className="w-6 h-6" />
          </button>
        </div>
        <div>{children}</div>
      </div>
    </div>
  );
};

export default Modal;

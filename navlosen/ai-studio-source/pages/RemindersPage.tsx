
import React, { useState } from 'react';
import { MOCK_REMINDERS } from '../constants';
import { Reminder } from '../types';
import Button from '../components/common/Button';
import Modal from '../components/common/Modal';
import { BellIcon, PlusCircleIcon, CheckCircleIcon, XCircleIcon } from '../components/icons';

const RemindersPage: React.FC = () => {
  const [reminders, setReminders] = useState<Reminder[]>(MOCK_REMINDERS);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newReminderTitle, setNewReminderTitle] = useState('');
  const [newReminderDate, setNewReminderDate] = useState('');
  const [newReminderDesc, setNewReminderDesc] = useState('');

  const toggleReminderStatus = (id: string) => {
    setReminders(prev => prev.map(r => r.id === id ? { ...r, completed: !r.completed } : r));
  };

  const handleAddReminder = () => {
    if (!newReminderTitle || !newReminderDate) {
      alert("Vennligst fyll ut tittel og dato for påminnelsen.");
      return;
    }
    const newReminder: Reminder = {
      id: `rem${Date.now()}`,
      title: newReminderTitle,
      dueDate: newReminderDate,
      description: newReminderDesc,
      completed: false,
    };
    setReminders(prev => [newReminder, ...prev].sort((a,b) => new Date(a.dueDate).getTime() - new Date(b.dueDate).getTime()));
    setIsModalOpen(false);
    setNewReminderTitle('');
    setNewReminderDate('');
    setNewReminderDesc('');
  };
  
  const deleteReminder = (id: string) => {
     if (window.confirm("Er du sikker på at du vil slette denne påminnelsen?")) {
        setReminders(prev => prev.filter(r => r.id !== id));
     }
  };

  const upcomingReminders = reminders.filter(r => !r.completed);
  const completedReminders = reminders.filter(r => r.completed);

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow flex justify-between items-center">
        <div>
          <h2 className="text-xl font-semibold text-darkgray mb-1">Mine Påminnelser</h2>
          <p className="text-mediumgray">Hold oversikt over viktige frister og gjøremål.</p>
        </div>
        <Button onClick={() => setIsModalOpen(true)} leftIcon={<PlusCircleIcon className="w-5 h-5"/>}>
          Ny Påminnelse
        </Button>
      </div>

      <div>
        <h3 className="text-lg font-semibold text-darkgray mb-3">Kommende Påminnelser ({upcomingReminders.length})</h3>
        {upcomingReminders.length > 0 ? (
          <ul className="space-y-3">
            {upcomingReminders.map(reminder => (
              <li key={reminder.id} className="bg-white p-4 rounded-lg shadow flex flex-col sm:flex-row justify-between items-start">
                <div className="flex-grow">
                  <h4 className="font-semibold text-darkgray">{reminder.title}</h4>
                  <p className="text-sm text-mediumgray">Frist: {new Date(reminder.dueDate).toLocaleDateString('nb-NO', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</p>
                  {reminder.description && <p className="text-sm text-gray-600 mt-1">{reminder.description}</p>}
                </div>
                <div className="mt-4 sm:mt-0 sm:ml-4 flex flex-col sm:flex-row items-stretch sm:items-center gap-2 flex-shrink-0">
                   <Button size="sm" variant="outline" onClick={() => alert('Funksjonalitet for "Legg i kalender" kommer snart.')}>
                    Legg i kalender
                  </Button>
                  <Button size="sm" variant="outline" onClick={() => alert('Funksjonalitet for "Skru på varsler" kommer snart.')}>
                    Skru på varsler
                  </Button>
                   <Button size="sm" variant="outline" onClick={() => toggleReminderStatus(reminder.id)} leftIcon={<CheckCircleIcon className="w-4 h-4"/>}>
                    Fullført
                  </Button>
                  <Button size="sm" variant="danger" onClick={() => deleteReminder(reminder.id)} leftIcon={<XCircleIcon className="w-4 h-4"/>}>
                    Slett
                  </Button>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <div className="bg-white p-6 rounded-lg shadow text-center">
            <BellIcon className="w-12 h-12 text-mediumgray mx-auto mb-3" />
            <p className="text-mediumgray">Du har ingen påminnelser ennå. Vil du legge inn første?</p>
          </div>
        )}
      </div>

      {completedReminders.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-darkgray mb-3 mt-8">Fullførte Påminnelser ({completedReminders.length})</h3>
          <ul className="space-y-3">
            {completedReminders.map(reminder => (
              <li key={reminder.id} className="bg-gray-50 p-4 rounded-lg shadow-sm flex justify-between items-center opacity-70">
                <div>
                  <h4 className="font-semibold text-gray-500 line-through">{reminder.title}</h4>
                  <p className="text-sm text-gray-400">Fullført: {new Date(reminder.dueDate).toLocaleDateString('nb-NO')}</p>
                </div>
                 <div className="flex items-center space-x-2 flex-shrink-0">
                  <Button size="sm" variant="outline" onClick={() => toggleReminderStatus(reminder.id)} leftIcon={<BellIcon className="w-4 h-4"/>}>
                    Merk som ufullstendig
                  </Button>
                   <Button size="sm" variant="danger" onClick={() => deleteReminder(reminder.id)} leftIcon={<XCircleIcon className="w-4 h-4"/>}>
                    Slett
                  </Button>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}

      <Modal title="Legg til Ny Påminnelse" isOpen={isModalOpen} onClose={() => setIsModalOpen(false)}>
        <div className="space-y-4">
          <div>
            <label htmlFor="reminderTitle" className="block text-sm font-medium text-darkgray">Tittel</label>
            <input 
              type="text" 
              id="reminderTitle"
              value={newReminderTitle}
              onChange={(e) => setNewReminderTitle(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm" 
            />
          </div>
          <div>
            <label htmlFor="reminderDate" className="block text-sm font-medium text-darkgray">Fristdato</label>
            <input 
              type="date" 
              id="reminderDate"
              value={newReminderDate}
              onChange={(e) => setNewReminderDate(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm" 
            />
          </div>
           <div>
            <label htmlFor="reminderDesc" className="block text-sm font-medium text-darkgray">Beskrivelse (valgfritt)</label>
            <textarea
              id="reminderDesc"
              rows={3}
              value={newReminderDesc}
              onChange={(e) => setNewReminderDesc(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm resize-y" 
            />
          </div>
          <div className="flex justify-end space-x-2">
            <Button variant="outline" onClick={() => setIsModalOpen(false)}>Avbryt</Button>
            <Button onClick={handleAddReminder}>Legg til Påminnelse</Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default RemindersPage;
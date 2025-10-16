
import React, { useState, useRef } from 'react';
import { MOCK_DOCUMENTS } from '../constants';
import { Document } from '../types';
import Button from '../components/common/Button';
// Modal and PlusCircleIcon are removed as the manual add functionality is removed.
import { DocumentTextIcon, ArrowUpTrayIcon, InformationCircleIcon, LockClosedIcon } from '../components/icons';

const DocumentsPage: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>(MOCK_DOCUMENTS);
  // Removed state and functions for manual modal:
  // const [isModalOpen, setIsModalOpen] = useState(false);
  // const [newDocumentName, setNewDocumentName] = useState('');
  // const [newDocumentType, setNewDocumentType] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // Simulate file upload
      const newDoc: Document = {
        id: `doc${Date.now()}`,
        name: file.name,
        type: file.type || 'Ukjent filtype',
        uploadDate: new Date().toLocaleDateString('nb-NO'),
        size: `${(file.size / (1024 * 1024)).toFixed(2)} MB`,
      };
      setDocuments(prev => [newDoc, ...prev]);
      // setIsModalOpen(false); // No longer needed
      // setNewDocumentName(''); // No longer needed
      // setNewDocumentType(''); // No longer needed
      alert(`Fil "${file.name}" er "lastet opp" (simulert). I en ekte applikasjon ville den blitt sendt til en sikker server.`);
       // Reset file input to allow uploading the same file again if needed
      if(fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };
  
  const openFileDialog = () => {
    fileInputRef.current?.click();
  }

  // Mock function for manual add, now removed:
  // const handleAddDocument = () => { ... };


  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow flex justify-between items-center">
        <div>
          <h2 className="text-xl font-semibold text-darkgray mb-1">Mine Dokumenter</h2>
          <p className="text-mediumgray">Sikker lagring og organisering av dine NAV-relaterte dokumenter.</p>
        </div>
        <Button onClick={openFileDialog} leftIcon={<ArrowUpTrayIcon className="w-5 h-5"/>}>
          Last Opp Dokument
        </Button>
        <input type="file" ref={fileInputRef} onChange={handleFileUpload} className="hidden" accept="application/pdf,image/*,.doc,.docx,.txt" />
      </div>

      <div className="p-4 bg-blue-50 border-l-4 border-primary text-primary-dark rounded-lg shadow text-sm">
        <div className="flex items-start">
          <LockClosedIcon className="w-5 h-5 mr-2 mt-0.5 flex-shrink-0" />
          <div>
            <p><span className="font-semibold">Pilotinformasjon:</span> I denne pilotversjonen lagres dokumenter kun midlertidig og vil bli slettet ved forespørsel eller ved pilotslutt.</p>
          </div>
        </div>
      </div>


      {documents.length > 0 ? (
        <div className="overflow-x-auto bg-white rounded-lg shadow">
          <table className="w-full text-sm text-left text-darkgray">
            <thead className="text-xs text-darkgray uppercase bg-lightgray">
              <tr>
                <th scope="col" className="px-6 py-3">Dokumentnavn</th>
                <th scope="col" className="px-6 py-3">Type</th>
                <th scope="col" className="px-6 py-3">Opplastingsdato</th>
                <th scope="col" className="px-6 py-3">Størrelse</th>
                <th scope="col" className="px-6 py-3">Handlinger</th>
              </tr>
            </thead>
            <tbody>
              {documents.map(doc => (
                <tr key={doc.id} className="bg-white border-b hover:bg-gray-50">
                  <td className="px-6 py-4 font-medium text-darkgray whitespace-nowrap flex items-center">
                    <DocumentTextIcon className="w-5 h-5 text-primary mr-2 flex-shrink-0" />
                    {doc.name}
                  </td>
                  <td className="px-6 py-4">{doc.type}</td>
                  <td className="px-6 py-4">{doc.uploadDate}</td>
                  <td className="px-6 py-4">{doc.size}</td>
                  <td className="px-6 py-4">
                    {/* Mock actions - implement as needed */}
                    <button className="font-medium text-primary hover:underline mr-2" onClick={() => alert(`Viser ${doc.name} (simulert)`)}>Vis</button>
                    <button 
                      className="font-medium text-red-500 hover:underline" 
                      onClick={() => {
                        if(window.confirm(`Er du sikker på at du vil slette "${doc.name}"?`)) {
                          setDocuments(prev => prev.filter(d => d.id !== doc.id));
                          alert(`"${doc.name}" slettet (simulert).`);
                        }
                      }}
                    >
                      Slett
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="bg-white p-10 rounded-lg shadow text-center">
          <DocumentTextIcon className="w-16 h-16 text-mediumgray mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-darkgray mb-2">Ingen dokumenter enda</h3>
          <p className="text-mediumgray mb-4">Trykk "Last Opp Dokument" for å samle alt på ett trygt sted.</p>
          <Button onClick={openFileDialog} leftIcon={<ArrowUpTrayIcon className="w-5 h-5"/>}>
            Last Opp Dokument
          </Button>
        </div>
      )}
      
       <div className="mt-6 p-4 bg-blue-50 border-l-4 border-primary text-primary-dark rounded-lg shadow">
        <div className="flex items-start">
          <InformationCircleIcon className="w-6 h-6 mr-2 flex-shrink-0" />
          <div>
            <h4 className="font-semibold">Sikkerhet og Personvern:</h4>
            <p className="text-sm">I en fullverdig versjon av NAV-Losen vil alle dokumenter lagres kryptert og sikkert i henhold til GDPR og norske personvernlover. Denne siden er en demonstrasjon.</p>
          </div>
        </div>
      </div>

      {/* Modal for adding document manually has been removed as it was not actively used by any UI element. */}

    </div>
  );
};

export default DocumentsPage;
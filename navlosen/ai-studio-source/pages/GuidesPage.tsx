
import React, { useState, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { MOCK_GUIDES, APP_ROUTES } from '../constants';
import { Guide } from '../types';
import { BookOpenIcon, ChevronRightIcon } from '../components/icons';

const GuidesPage: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('Alle');

  const categories = useMemo(() => 
    ['Alle', ...new Set(MOCK_GUIDES.map(guide => guide.category))]
  , []);

  const filteredGuides = useMemo(() => 
    MOCK_GUIDES.filter(guide =>
      (guide.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
       guide.summary.toLowerCase().includes(searchTerm.toLowerCase())) &&
      (selectedCategory === 'Alle' || guide.category === selectedCategory)
    )
  , [searchTerm, selectedCategory]);

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold text-darkgray mb-4">Veiledninger</h2>
        <p className="text-mediumgray mb-4">Finn steg-for-steg veiledninger for ulike NAV-ytelser og prosesser. Velg en kategori eller søk etter nøkkelord.</p>
        
        <div className="flex flex-col md:flex-row gap-4 mb-6">
          <input
            type="text"
            placeholder="Søk i veiledninger..."
            className="flex-grow p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            aria-label="Søk i veiledninger"
          />
          <select
            className="p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent bg-white"
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            aria-label="Filtrer veiledninger etter kategori"
          >
            {categories.map(category => (
              <option key={category} value={category}>{category}</option>
            ))}
          </select>
        </div>
      </div>

      {filteredGuides.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredGuides.map((guide: Guide) => (
            <Link 
              key={guide.id} 
              to={`${APP_ROUTES.GUIDES}/${guide.id}`}
              className="bg-white p-6 rounded-lg shadow hover:shadow-xl transition-shadow duration-200 flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center text-secondary mb-2">
                  <BookOpenIcon className="w-6 h-6 mr-2" />
                  <h3 className="text-lg font-semibold text-darkgray">{guide.title}</h3>
                </div>
                 <p className="text-xs text-mediumgray mb-3">Kategori: {guide.category}</p>
                 <p className="text-mediumgray text-sm mb-4">{guide.summary}</p>

                 {/* New Metadata */}
                <div className="space-y-2 text-xs border-t pt-3">
                    {guide.timeEstimate && <p><span className="font-semibold">Tidsbruk:</span> {guide.timeEstimate}</p>}
                    {guide.requirements && <p><span className="font-semibold">Hva du trenger:</span> {guide.requirements}</p>}
                </div>
              </div>
              <div className="flex items-center text-primary hover:underline mt-4">
                Gå til første steg <ChevronRightIcon className="w-4 h-4 ml-1" />
              </div>
            </Link>
          ))}
        </div>
      ) : (
        <div className="bg-white p-6 rounded-lg shadow text-center">
          <p className="text-mediumgray">Ingen veiledninger funnet som passer ditt søk eller valgte kategori.</p>
        </div>
      )}
    </div>
  );
};

export default GuidesPage;
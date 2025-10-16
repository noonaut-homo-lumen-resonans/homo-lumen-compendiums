
import React from 'react';
import { BriefcaseIcon, DocumentTextIcon, ChevronRightIcon, InformationCircleIcon } from '../components/icons';
import Button from '../components/common/Button';
import { MOCK_JOB_POSTINGS, MOCK_JOB_APPLICATIONS } from '../constants';

const JobPage: React.FC = () => {

    const applicationStatusColors: { [key: string]: string } = {
        'Søknad sendt': 'bg-blue-100 text-blue-800',
        'Under vurdering': 'bg-yellow-100 text-yellow-800',
        'Intervju': 'bg-green-100 text-green-800',
        'Avslag': 'bg-red-100 text-red-800',
    };

  return (
    <div className="space-y-6">
      
      {/* Future Vision Banner */}
      <div className="p-4 bg-yellow-100 border-l-4 border-yellow-500 text-yellow-800 rounded-lg shadow">
        <div className="flex items-start">
          <InformationCircleIcon className="w-6 h-6 mr-3 flex-shrink-0" />
          <div>
            <h4 className="font-bold">Fremtidsvisjon - Konsept</h4>
            <p className="text-sm">Denne siden er et konsept for en fremtidig funksjon og er ikke aktiv i denne piloten. Den viser hvordan NAV-Losen kan hjelpe deg med jobbsøk i neste fase.</p>
          </div>
        </div>
      </div>
      
      <div className="bg-white p-6 rounded-lg shadow flex justify-between items-center">
        <div>
          <h2 className="text-xl font-semibold text-darkgray mb-1">Jobbsøk</h2>
          <p className="text-mediumgray">Verktøy for å bygge CV, finne jobber og holde orden på søknader.</p>
        </div>
      </div>

      {/* CV Section */}
      <div className="bg-white p-6 rounded-lg shadow opacity-50">
        <h3 className="text-lg font-semibold text-darkgray mb-3 flex items-center">
          <DocumentTextIcon className="w-6 h-6 text-gray-500 mr-2" />
          Min CV
        </h3>
        <p className="text-mediumgray mb-4">Bygg en profesjonell CV som er klar til å sendes til arbeidsgivere.</p>
        <div className="flex flex-col sm:flex-row gap-3">
             <Button disabled>Rediger CV</Button>
             <Button variant="outline" disabled>Last ned som PDF</Button>
        </div>
      </div>

       {/* My Applications Section */}
      <div className="bg-white p-6 rounded-lg shadow opacity-50">
        <h3 className="text-lg font-semibold text-darkgray mb-4">Mine Jobbsøknader</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left text-darkgray">
            <thead className="text-xs text-darkgray uppercase bg-lightgray">
              <tr>
                <th scope="col" className="px-4 py-3">Stilling</th>
                <th scope="col" className="px-4 py-3">Bedrift</th>
                <th scope="col" className="px-4 py-3">Status</th>
                <th scope="col" className="px-4 py-3">Dato</th>
              </tr>
            </thead>
            <tbody>
              {MOCK_JOB_APPLICATIONS.map(app => (
                <tr key={app.id} className="bg-white border-b">
                  <td className="px-4 py-4 font-medium">{app.jobTitle}</td>
                  <td className="px-4 py-4">{app.company}</td>
                  <td className="px-4 py-4">
                     <span className={`px-2 py-1 text-xs font-semibold rounded-full ${applicationStatusColors[app.status]}`}>
                      {app.status}
                    </span>
                  </td>
                  <td className="px-4 py-4">{app.dateApplied}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Job Postings Section */}
      <div className="bg-white p-6 rounded-lg shadow opacity-50">
        <h3 className="text-lg font-semibold text-darkgray mb-3 flex items-center">
            <BriefcaseIcon className="w-6 h-6 text-gray-500 mr-2" />
            Ledige Stillinger (fra NAV)
        </h3>
        <div className="space-y-4">
            {MOCK_JOB_POSTINGS.map(job => (
                 <div key={job.id} className="p-4 border rounded-lg flex justify-between items-center">
                    <div>
                        <h4 className="font-semibold text-darkgray">{job.title}</h4>
                        <p className="text-sm text-mediumgray">{job.company} - {job.location}</p>
                    </div>
                    <Button size="sm" variant="secondary" rightIcon={<ChevronRightIcon className="w-4 h-4"/>} disabled>
                        Se stilling
                    </Button>
                 </div>
            ))}
        </div>
      </div>

    </div>
  );
};

export default JobPage;

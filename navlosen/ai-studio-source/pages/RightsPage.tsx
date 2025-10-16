import React from 'react';
import { ScaleIcon, InformationCircleIcon } from '../components/icons';

// New interfaces for a nested structure
interface SubCategory {
  title: string;
  points: string[];
}

interface MainCategory {
  title: string;
  subCategories: SubCategory[];
}

// Populate with the user's detailed content
const rightsData: MainCategory[] = [
  {
    title: "GENERELLE RETTIGHETER I NAV-SYSTEMET",
    subCategories: [
      {
        title: "Rett til informasjon og veiledning",
        points: [
          "Få hjelp til å forstå dine rettigheter og plikter",
          "Få søknadsskjema og veiledning på ditt språk",
        ],
      },
      {
        title: "Rett til å bli behandlet med respekt",
        points: [
          "Høflig og profesjonell behandling fra alle NAV-ansatte",
        ],
      },
      {
        title: "Rett til innsyn i din egen sak",
        points: [
          "Se alle dokumenter i din sak (med noen unntak)",
          "Få kopi av dokumenter som gjelder deg",
        ],
      },
      {
        title: "Rett til å klage på vedtak",
        points: [
          "Klagefristen er vanligvis 3 uker fra du mottok vedtaket",
          "Du har rett til å se sakens dokumenter før du klager",
        ],
      },
      {
        title: "Rett til å ha med deg en hjelpeperson",
        points: [
          "Til møter med NAV",
          "Personen kan være familiemedlem, venn eller advokat",
        ],
      },
       {
        title: "Tilgjengelighet og Personvern",
        points: [
            "Rett til tolk hvis du trenger det",
            "NAV sine tjenester skal være tilgjengelige for alle (universell utforming)",
            "Rett til innsyn, retting og sletting av dine personopplysninger (GDPR)",
        ]
      }
    ],
  },
  {
    title: "SØKNAD OG SAKSBEHANDLING",
    subCategories: [
      {
        title: "Rett til forsvarlig saksbehandling",
        points: [
          "NAV skal vurdere saken din på nytt hvis du ber om det",
          "Å få skriftlig begrunnelse for vedtak",
        ],
      },
      {
        title: "Rett til å få hjulpet deg med søknaden",
        points: [
          "NAV kan hjelpe deg å fylle ut søknadsskjema",
          "Rett til veiledning om hvilke dokumenter du trenger",
        ],
      },
    ],
  },
  {
    title: "DINE PLIKTER OVERFOR NAV",
    subCategories: [
      {
        title: "Opplysningsplikt",
        points: [
          "Du må gi NAV alle opplysninger som har betydning for saken din",
          "Du må gi beskjed om endringer som kan påvirke ytelsen (f.eks. jobb, inntekt, bosted, sivilstatus)",
          "Du må levere dokumentasjon NAV ber om for å behandle saken din",
        ],
      },
      {
        title: "Møteplikt",
        points: [
          "Du må møte til avtaler og aktiviteter NAV kaller deg inn til",
          "Gi beskjed på forhånd hvis du ikke kan møte",
        ],
      },
      {
        title: "Aktivitetsplikt (gjelder enkelte ytelser)",
        points: [
          "Være reell arbeidssøker hvis du mottar dagpenger",
          "Delta i aktiviteter NAV mener kan hjelpe deg tilbake til arbeid",
        ],
      },
      {
        title: "Tilbakebetalingsplikt",
        points: [
          "Betale tilbake penger du har fått for mye",
          "Dette gjelder selv om feilen ikke var din",
        ],
      },
    ],
  },
  {
    title: "SÆRLIGE RETTIGHETER VED SYKDOM/UFØRHET",
    subCategories: [
      {
        title: "Rett til medvirkning",
        points: [
          "Delta i utforming av din oppfølgingsplan",
          "Gi innspill til hvilke tiltak som passer for deg",
        ],
      },
      {
        title: "Rett til individuell vurdering",
        points: [
          "Saken din skal vurderes ut fra dine individuelle forhold",
          "Ikke bare etter standardmaler",
        ],
      },
    ],
  },
  {
    title: "ØKONOMISK STØNAD",
    subCategories: [
      {
        title: "Rett til forskudd",
        points: [
          "I særlige tilfeller kan du få forskudd på ytelser",
          "Gjelder når du venter på saksbehandling",
        ],
      },
      {
        title: "Rett til økonomisk sosialhjelp som siste utvei",
        points: [
          "Når du ikke har andre muligheter til å forsørge deg",
          "Kommunen har ansvaret, ikke NAV",
        ],
      },
    ],
  },
];

const RightsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center mb-4">
          <ScaleIcon className="w-8 h-8 text-primary mr-3" />
          <h2 className="text-xl font-semibold text-darkgray">Dine Rettigheter og Plikter</h2>
        </div>
        <p className="text-mediumgray">
          Det er viktig å kjenne til dine rettigheter og plikter når du er i kontakt med NAV. 
          Denne siden gir en generell oversikt.
        </p>
      </div>

      {rightsData.map((mainCategory, index) => (
        <div key={index} className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-xl font-semibold text-darkgray mb-4">{mainCategory.title}</h3>
          <div className="space-y-4">
            {mainCategory.subCategories.map((subCategory, subIndex) => (
              <div key={subIndex}>
                <h4 className="text-md font-semibold text-gray-700 mb-2">{subCategory.title}</h4>
                <ul className="list-disc list-inside space-y-1 text-mediumgray pl-4">
                  {subCategory.points.map((point, pIndex) => (
                    <li key={pIndex}>{point}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      ))}
      
      <div className="mt-6 p-4 bg-blue-50 border-l-4 border-primary text-primary-dark rounded-lg shadow">
        <div className="flex items-start">
          <InformationCircleIcon className="w-6 h-6 mr-2 flex-shrink-0" />
          <div>
            <h4 className="font-semibold">Viktig:</h4>
            <p className="text-sm">Denne oversikten gir generell informasjon. For fullstendig og juridisk bindende informasjon, se alltid nav.no eller kontakt NAV direkte. Reglene kan endre seg, og din individuelle situasjon kan påvirke hvilke rettigheter og plikter som gjelder.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RightsPage;
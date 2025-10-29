
import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { MOCK_GUIDES, APP_ROUTES } from '../constants';
import { Guide } from '../types';
import Button from '../components/common/Button';
import { InformationCircleIcon } from '../components/icons';


const parseInlineText = (text: string): React.ReactNode[] => {
  const elements: React.ReactNode[] = [];
  let remainingText = text;
  let keyIndex = 0;

  // Order of regex matters: handle links first, then bold
  const linkRegex = /\[(.*?)\]\((.*?)\)/;
  const boldRegex = /\*\*(.*?)\*\*/;

  while (remainingText.length > 0) {
    const linkMatch = remainingText.match(linkRegex);
    const boldMatch = remainingText.match(boldRegex);

    let earliestMatch: { type: 'link' | 'bold'; match: RegExpMatchArray } | null = null;

    if (linkMatch && boldMatch) {
      earliestMatch = linkMatch.index! < boldMatch.index! 
        ? { type: 'link', match: linkMatch } 
        : { type: 'bold', match: boldMatch };
    } else if (linkMatch) {
      earliestMatch = { type: 'link', match: linkMatch };
    } else if (boldMatch) {
      earliestMatch = { type: 'bold', match: boldMatch };
    }

    if (earliestMatch) {
      const matchIndex = earliestMatch.match.index!;
      // Add text before match
      if (matchIndex > 0) {
        elements.push(remainingText.substring(0, matchIndex));
      }
      // Add matched element
      if (earliestMatch.type === 'link') {
        elements.push(
          <a key={`link-${keyIndex++}`} href={earliestMatch.match[2]} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">
            {earliestMatch.match[1]}
          </a>
        );
      } else { // bold
        elements.push(<strong key={`bold-${keyIndex++}`}>{earliestMatch.match[1]}</strong>);
      }
      remainingText = remainingText.substring(matchIndex + earliestMatch.match[0].length);
    } else {
      // No more matches, add remaining text
      elements.push(remainingText);
      remainingText = '';
    }
  }
  return elements;
};


const BasicMarkdown: React.FC<{ content: string }> = ({ content }) => {
  const lines = content.split(/\r?\n/); // Corrected line splitting
  const elements: JSX.Element[] = [];
  let currentList: { type: 'ul' | 'ol'; items: React.ReactNode[][] } | null = null;

  const flushList = () => {
    if (currentList) {
      if (currentList.type === 'ul') {
        elements.push(
          <ul key={`ul-${elements.length}`} className="list-disc pl-6 space-y-1 my-3 text-mediumgray">
            {currentList.items.map((itemContent, idx) => <li key={idx}>{itemContent}</li>)}
          </ul>
        );
      } else {
        elements.push(
          <ol key={`ol-${elements.length}`} className="list-decimal pl-6 space-y-1 my-3 text-mediumgray">
            {currentList.items.map((itemContent, idx) => <li key={idx}>{itemContent}</li>)}
          </ol>
        );
      }
      currentList = null;
    }
  };

  lines.forEach((line, index) => {
    const trimmedLine = line.trim();
    if (trimmedLine.startsWith('# ')) {
      flushList();
      elements.push(<h1 key={index} className="text-3xl font-bold mt-6 mb-3 text-darkgray">{parseInlineText(trimmedLine.substring(2))}</h1>);
    } else if (trimmedLine.startsWith('## ')) {
      flushList();
      elements.push(<h2 key={index} className="text-2xl font-semibold mt-5 mb-2 text-darkgray">{parseInlineText(trimmedLine.substring(3))}</h2>);
    } else if (trimmedLine.startsWith('### ')) {
      flushList();
      elements.push(<h3 key={index} className="text-xl font-semibold mt-4 mb-1 text-darkgray">{parseInlineText(trimmedLine.substring(4))}</h3>);
    } else if (trimmedLine.startsWith('- ')) {
      if (currentList?.type !== 'ul') {
        flushList();
        currentList = { type: 'ul', items: [] };
      }
      currentList.items.push(parseInlineText(trimmedLine.substring(2)));
    } else if (trimmedLine.match(/^\d+\.\s/)) {
      if (currentList?.type !== 'ol') {
        flushList();
        currentList = { type: 'ol', items: [] };
      }
      currentList.items.push(parseInlineText(trimmedLine.substring(trimmedLine.indexOf(' ') + 1)));
    } else {
      flushList();
      if (trimmedLine === '') {
         // Preserve empty lines for paragraph breaks if desired, or handle differently
         // For now, multiple empty lines won't create multiple <br> unless specifically handled
        if (elements.length > 0 && elements[elements.length -1].type !== 'br') { // Avoid multiple <br>
            // elements.push(<br key={`br-${index}`} />);
        }
      } else {
        elements.push(<p key={index} className="text-mediumgray mb-3 leading-relaxed">{parseInlineText(trimmedLine)}</p>);
      }
    }
  });

  flushList(); // Ensure any trailing list is rendered

  return <>{elements}</>;
};

const ScrollToTopButton: React.FC = () => {
    const [isVisible, setIsVisible] = useState(false);

    const toggleVisibility = () => {
        if (window.pageYOffset > 300) {
            setIsVisible(true);
        } else {
            setIsVisible(false);
        }
    };

    const scrollToTop = () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    };

    useEffect(() => {
        window.addEventListener('scroll', toggleVisibility);
        return () => {
            window.removeEventListener('scroll', toggleVisibility);
        };
    }, []);

    return (
        <button
            type="button"
            onClick={scrollToTop}
            className={`fixed bottom-24 right-6 bg-primary text-white p-3 rounded-full shadow-lg transition-opacity ${isVisible ? 'opacity-100' : 'opacity-0'}`}
            aria-label="Gå til toppen"
        >
             <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-6 h-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 15.75l7.5-7.5 7.5 7.5" />
            </svg>
        </button>
    );
};


const GuideDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const guide = MOCK_GUIDES.find((g: Guide) => g.id === id);

  if (!guide) {
    return (
      <div className="bg-white p-6 rounded-lg shadow text-center">
        <h2 className="text-xl font-semibold text-red-500 mb-4">Veiledning Ikke Funnet</h2>
        <p className="text-mediumgray">Beklager, vi kunne ikke finne veiledningen du leter etter.</p>
        <Link to={APP_ROUTES.GUIDES} className="mt-4 inline-block px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark">
          Tilbake til Veiledninger
        </Link>
      </div>
    );
  }

  return (
    <div className="bg-white p-8 rounded-lg shadow-xl">
      <header className="mb-6 border-b pb-4">
        <div className="flex justify-between items-start">
            <div>
                 <h1 className="text-3xl font-bold text-darkgray mb-2">{guide.title}</h1>
                <p className="text-sm text-mediumgray">Kategori: {guide.category} | Sist oppdatert: {guide.lastUpdated}</p>
            </div>
            <Button variant="outline" size="sm" onClick={() => alert('Funksjonalitet for å vise en forenklet versjon kommer snart.')}>
                Vis Enkel Norsk
            </Button>
        </div>
      </header>
      
      <p className="italic text-mediumgray mb-6">"Vi tar deg gjennom én ting av gangen. Du kan alltid hoppe over og komme tilbake."</p>

      {guide.requirements && (
        <div className="mb-6 p-4 bg-blue-50 border-l-4 border-primary text-primary-dark rounded-lg shadow-sm">
            <div className="flex items-start">
            <InformationCircleIcon className="w-6 h-6 mr-2 flex-shrink-0" />
            <div>
                <h4 className="font-semibold">Nyttig å ha klart:</h4>
                <p className="text-sm">{guide.requirements}</p>
            </div>
            </div>
        </div>
      )}

      <article className="prose prose-lg max-w-none">
        <BasicMarkdown content={guide.content} />
      </article>

      <div className="mt-8 pt-6 border-t">
        <Link to={APP_ROUTES.GUIDES} className="text-primary hover:underline">
          &larr; Tilbake til alle veiledninger
        </Link>
      </div>
      <ScrollToTopButton />
    </div>
  );
};

export default GuideDetailPage;
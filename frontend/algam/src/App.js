// import logo from './logo.svg';
import './index.css';
import WordCloud from 'react-wordcloud';

function App() {

  const words = [
    { text: 'React', value: 1000 },
    { text: 'JavaScript', value: 900 },
    { text: 'Node', value: 800 },
    { text: 'Express', value: 700 },
    { text: 'HTML', value: 600 },
    { text: 'CSS', value: 500 },
    { text: 'Web', value: 400 },
    { text: 'Development', value: 300 },
    { text: 'Programming', value: 200 },
    { text: 'Code', value: 100 },
  ];

  return (
    <div style={{ height: '100vh', width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
      <WordCloud words={words} />
    </div>
  );
}

export default App;

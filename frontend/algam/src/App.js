import React, { useState, useEffect } from 'react';
import WordCloud from 'react-wordcloud';
import 'tippy.js/dist/tippy.css'; // Optional for tooltips

function App() {
  const [words, setWords] = useState([]);

  useEffect(() => {
    // Function to fetch words data
    const fetchWords = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/topics/25');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        // Assume the response structure is as described and extract topics
        const topics = data[0].topics.map(topic => ({
          text: topic.name,
          value: Math.floor(Math.random() * 100) + 50 // Assigning random values for demonstration
        }));
        setWords(topics);
      } catch (error) {
        console.error('Failed to fetch words:', error);
      }
    };

    fetchWords();
  }, []); // The empty array ensures this effect only runs once when the component mounts

  const options = {
    colors: ['#FF6347', '#FFA500', '#32CD32', '#FFD700', '#FF4500', '#00FFFF'], // Tomato, Orange, LimeGreen, Gold, OrangeRed, Cyan
    enableTooltip: true,
    deterministic: false,
    fontFamily: 'impact',
    fontSizes: [20, 60],
    fontStyle: 'normal',
    // fontWeight: 'bold',
    padding: 1,
    rotations: 3,
    rotationAngles: [0, 90],
    scale: 'sqrt',
    spiral: 'archimedean',
    transitionDuration: 1000,
    backgroundColor: 'black', // WordCloud background color
  };

  return (
    <div style={{ height: '100vh', width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center', backgroundColor: 'black' }}>
      <WordCloud words={words} options={options} />
    </div>
  );
}

export default App;

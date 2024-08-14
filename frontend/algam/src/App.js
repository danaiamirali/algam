import React, { useState, useEffect } from 'react';
import WordCloud from 'react-wordcloud';
import 'tippy.js/dist/tippy.css'; // Optional for tooltips

function App() {
  const [words, setWords] = useState([]);
  const fetchInterval = 5 * 60 * 1000; // Set the interval time in milliseconds (e.g., 5 minutes)

  useEffect(() => {
    // Function to fetch words data
    const fetchWords = async () => {
      try {
        console.log("Fetching topics...")
        const response = await fetch('https://algam.onrender.com/topics/25');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        // Assume the response structure is as described and extract topics
        const topics = data[0].topics.map(topic => ({
          text: topic.name,
          value: topic.popularity
        }));
        setWords(topics);
      } catch (error) {
        console.error('Failed to fetch words:', error);
      }
    };

    // Initial fetch when the component mounts
    fetchWords();

    // Set up the interval to fetch data every X minutes
    const intervalId = setInterval(() => {
      fetchWords();
    }, fetchInterval);

    // Clear the interval when the component unmounts
    return () => clearInterval(intervalId);
  }, [fetchInterval]); // Dependency array includes fetchInterval to ensure it gets re-evaluated if changed

  const options = {
    colors: ['#FF6347', '#FFA500', '#32CD32', '#FFD700', '#FF4500', '#00FFFF'], // Tomato, Orange, LimeGreen, Gold, OrangeRed, Cyan
    enableTooltip: true,
    deterministic: false,
    fontFamily: 'impact',
    fontSizes: [20, 60],
    fontStyle: 'normal',
    padding: 1,
    rotations: 3,
    rotationAngles: [0, 90],
    scale: 'sqrt',
    spiral: 'archimedean',
    transitionDuration: 1000,
    backgroundColor: 'black', // WordCloud background color
  };

  const callbacks = {
    onWordClick: word => {
      const googleSearchUrl = `https://www.google.com/search?q=${encodeURIComponent(word.text)}`;
      window.open(googleSearchUrl, '_blank');
    },
  };

  return (
    <div style={{ height: '100vh', width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center', backgroundColor: 'black' }}>
      <WordCloud words={words} options={options} callbacks={callbacks} />
    </div>
  );
}

export default App;

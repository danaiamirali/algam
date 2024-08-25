import React, { useState, useEffect } from 'react';
import WordCloud from 'react-wordcloud';
import 'tippy.js/dist/tippy.css'; // Optional for tooltips

const Navbar = () => {
  const navbarStyle = {
    width: '100%',
    height: '50px', // Adjust the height as needed
    backgroundColor: 'white',
    position: 'fixed', // Fixes the navbar at the top of the viewport
    top: 0,
    left: 0,
    zIndex: 1000, // Ensures the navbar is on top of other elements
    display: 'flex',
    // justifyContent: 'center', // Centers content horizontally
    alignItems: 'center', // Centers content vertically
    boxShadow: '0px 2px 5px rgba(0, 0, 0, 0.1)', // Optional: adds a subtle shadow for depth
  };

  const logoStyle = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)', // Centers the logo both horizontally and vertically
    height: '40px', // Adjust the height of the logo as needed
  };

  return (
    <div style={navbarStyle}>
      <img 
        src="/logo.png" // Directly reference the image from the public folder
        alt="Website Logo" 
        style={logoStyle}
      />
    </div>
  );
};

function App() {
  const [words, setWords] = useState([]);

  useEffect(() => {
    // Function to fetch words data
    const fetchWords = async () => {
      try {
        const response = await fetch('https://octopus-app-myw9k.ondigitalocean.app/topics/20');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log('Fetched words:', data);
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

    fetchWords();
  }, []); // The empty array ensures this effect only runs once when the component mounts

  const options = {
    colors: ['#FFFFFF', '#F2C14E', '#F55536'], // Misty rose, Saffron, Tomato
    enableTooltip: true,
    deterministic: false,
    fontFamily: 'tahoma',
    fontSizes: [20, 60],
    fontStyle: 'normal',
    // fontWeight: 'bold',
    padding: 1,
    rotations: 1,
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
    <div style={{ paddingTop: '50px', height: '100vh', width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center', backgroundColor: 'black' }}>
      <Navbar />
      <WordCloud words={words} options={options} callbacks={callbacks} />
    </div>
  );
}

export default App;
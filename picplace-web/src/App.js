import React, {useEffect, useState} from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [posts, setPosts] = useState([])


  /* const performLookup = () => {} is an arrow function
  it's the same as function performLooup () {}
  you use arrow functions to make the code shorter
  */
  useEffect(() => {
    // do lookup for posts
    const postItems = [{"content": 2}, {"content": "Hello"}]
    setPosts(postItems)
  }, [])
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <p>
          {posts.map((post, index) => {
            return <li>{post.content}</li>
          })}
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;

import React from 'react';

const ResultComponent = ({ tokens }) => {
  return (
      <div className="tokens">
        {tokens && tokens.map((token, index) => (
          <span key={index} className="token">{token}<br></br></span>
        ))}
      </div>
  );
}

export default ResultComponent;

import React from 'react';

const ResultComponent = ({ result, tokens }) => {
  return (
    <div className="result">
      <div className="result-value">{result}</div>
    </div>
  );
}

export default ResultComponent;

import React, { Component } from 'react';
import './App.css';
import ResultComponent from './components/ResultComponent';
import ResultTokens from './components/ResultTokens';
import KeyPadComponent from './components/KeyPadComponent';

class App extends Component {
  state = {
    result: "",
    tokens: null
  }

  onClick = button => {
    if(button === "=") {
      this.calculate();
    }

    else if(button === "C") {
      this.reset();
    }

    else if(button === "CE") {
      this.backspace();
    }

    else {
      this.setState({
        result: this.state.result + button
      })
    }
  };

  calculate = () => {
    const operation = {
        "expression": this.state.result,
    };
    fetch("http://127.0.0.1:5000/api/calculate", {
        method: "POST",
        mode: 'cors',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(operation),
        redirect: "follow"
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            console.log(data)
            this.setState({
                result: data.result,
                tokens: data.tokens
            });
            console.log(data.tokens)
        } else {
            throw new Error(data.error || 'Unknown error');
        }
    })
    .catch(error => {
        console.error("Error:", error);
        this.setState({ result: "Error", tokens: null });
    });
};

  reset = () => {
    this.setState({
      result: "",
      tokens: null
    })
  };

  backspace = () => {
    this.setState({
      result: this.state.result.slice(0, -1)
    })
  };

  render() {
    return (
      <div>
        <div className="calculator-body">
          <h1>Simple Calculator</h1>
          <ResultComponent result={this.state.result} />
          <KeyPadComponent onClick={this.onClick} />
          <ResultTokens tokens= {this.state.tokens} />
        </div>
      </div>
    )
  }
}

export default App;
